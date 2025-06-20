from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Avg, Max
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .models import Lesson, Trainer, NewsPost, Payment, UserProfile, Horse, Resource
from django.http import HttpResponse, HttpRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from .serializers import NewsPostSerializer, TrainerSerializer, HorseSerializer, LessonSerializer, PaymentSerializer
import tempfile
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import NewsPostFilter, TrainerFilter, HorseFilter, LessonFilter, PaymentFilter
from typing import Any
from silk.profiling.profiler import silk_profile


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Главная страница приложения с информацией о доступных API endpoints.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Главная страница с информацией об API
    """
    
    stats_html = ""
    try:
        horses_count = Horse.objects.count()
        trainers_count = Trainer.objects.count()
        news_count = NewsPost.objects.filter(is_active=True).count()
        lessons_count = Lesson.objects.count()
        payments_count = Payment.objects.count()
        
        stats_html = f"""
        <h2>📊 Статистика базы данных:</h2>
        <ul>
            <li>Лошадей: {horses_count}</li>
            <li>Тренеров: {trainers_count}</li>
            <li>Новостей: {news_count}</li>
            <li>Занятий: {lessons_count}</li>
            <li>Платежей: {payments_count}</li>
        </ul>
        """
    except Exception as e:
        stats_html = f"<h2>📊 Статистика базы данных:</h2><p>Ошибка при получении статистики: {e}</p>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Horse Stable API</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; padding: 2em; background-color: #f4f4f9; color: #333; }}
            .container {{ max-width: 800px; margin: 0 auto; background-color: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1, h2 {{ color: #444; border-bottom: 2px solid #eee; padding-bottom: 0.3em;}}
            h1 {{ font-size: 2.5em; text-align: center; }}
            ul {{ list-style-type: none; padding-left: 0; }}
            li {{ margin-bottom: 0.7em; background-color: #fafafa; padding: 0.5em 1em; border-radius: 4px; border-left: 4px solid #007bff;}}
            a {{ color: #007bff; text-decoration: none; font-weight: 500;}}
            a:hover {{ text-decoration: underline; }}
            strong {{ color: #555; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐎 Horse Stable API</h1>
        
            <h2>📚 Доступные API Endpoints:</h2>
            <ul>
                <li><strong>Новости:</strong> <a href="/api/news/">/api/news/</a></li>
                <li><strong>Тренеры:</strong> <a href="/api/trainers/">/api/trainers/</a></li>
                <li><strong>Лошади:</strong> <a href="/api/horses/">/api/horses/</a></li>
                <li><strong>Занятия:</strong> <a href="/api/lessons/">/api/lessons/</a></li>
                <li><strong>Платежи:</strong> <a href="/api/payments/">/api/payments/</a></li>
            </ul>
            
            <h2>🔧 Инструменты мониторинга:</h2>
            <ul>
                <li><strong>Django Silk (профилирование):</strong> <a href="/silk/">/silk/</a></li>
                <li><strong>Django Admin:</strong> <a href="/admin/">/admin/</a></li>
            </ul>
            
            <h2>🧪 Тестовые endpoints:</h2>
            <ul>
                <li><strong>Sentry Error Test:</strong> <a href="/sentry/test-error/">/sentry/test-error/</a></li>
                <li><strong>Sentry Performance Test:</strong> <a href="/sentry/test-performance/">/sentry/test-performance/</a></li>
                <li><strong>Sentry User Context Test:</strong> <a href="/sentry/test-user-context/">/sentry/test-user-context/</a></li>
                <li><strong>Silk Slow Query Test:</strong> <a href="/silk/test-slow-query/">/silk/test-slow-query/</a></li>
                <li><strong>Silk Memory Usage Test:</strong> <a href="/silk/test-memory-usage/">/silk/test-memory-usage/</a></li>
                <li><strong>Silk Database Queries Test:</strong> <a href="/silk/test-database-queries/">/silk/test-database-queries/</a></li>
            </ul>
            
            {stats_html}
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html_content)


# API ViewSets
class NewsPostViewSet(viewsets.ModelViewSet):
    """
    API ViewSet для новостей с поддержкой фильтрации, поиска и сортировки.
    """
    queryset = NewsPost.objects.filter(is_active=True)
    serializer_class = NewsPostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NewsPostFilter
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'published_at', 'title']
    ordering = ['-published_at']


class TrainerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet для просмотра тренеров с поддержкой фильтрации, поиска и сортировки.
    """
    queryset = Trainer.objects.all().annotate(
        lessons_count=Count('lessons')
    )
    serializer_class = TrainerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TrainerFilter
    search_fields = ['first_name', 'last_name', 'bio']
    ordering_fields = ['experience_years', 'first_name', 'last_name']
    ordering = ['-experience_years']

    def get_serializer_context(self) -> dict[str, Any]:
        """
        Добавляет в контекст сериализатора ID "топовых" тренеров.
        """
        context = super().get_serializer_context()
        top_trainers = Trainer.objects.order_by('-experience_years')[:5].values_list('id', flat=True)
        context['top_trainer_ids'] = list(top_trainers)
        return context


class HorseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet для просмотра лошадей с поддержкой фильтрации, поиска и сортировки.
    """
    queryset = Horse.objects.all()
    serializer_class = HorseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HorseFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'birth_date', 'gender']
    ordering = ['name']


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet для просмотра занятий с поддержкой фильтрации, поиска и сортировки.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LessonFilter
    search_fields = ['horse__name', 'trainer__first_name', 'trainer__last_name', 'student__user__username']
    ordering_fields = ['date', 'price', 'status']
    ordering = ['-date']

    def get_serializer_context(self) -> dict[str, Any]:
        """
        Добавляет в контекст сериализатора среднюю цену за урок.
        """
        context = super().get_serializer_context()
        avg_price_data = Lesson.objects.aggregate(avg_price=Avg('price'))
        context['average_price'] = avg_price_data['avg_price'] or 0
        return context


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet для просмотра платежей с поддержкой фильтрации, поиска и сортировки.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PaymentFilter
    search_fields = ['user__username', 'purpose']
    ordering_fields = ['timestamp', 'amount', 'status']
    ordering = ['-timestamp']


# Sentry Test Views
def test_sentry_error(request: HttpRequest) -> HttpResponse:
    """
    Тестовое представление для проверки Sentry.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Ответ с информацией об ошибке
    """
    try:
        # Имитация ошибки
        raise ValueError("Тестовая ошибка для Sentry")
    except ValueError as e:
        import sentry_sdk
        sentry_sdk.capture_exception(e)
        return HttpResponse("Ошибка отправлена в Sentry")


def test_sentry_performance(request: HttpRequest) -> HttpResponse:
    """
    Тестовое представление для проверки производительности в Sentry.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Ответ с информацией о производительности
    """
    import time
    import sentry_sdk
    
    with sentry_sdk.start_transaction(op="test", name="test_performance"):
        time.sleep(0.1)  # Имитация медленной операции
        
        with sentry_sdk.start_span(op="db", description="test_query"):
            horses = Horse.objects.all()
            count = horses.count()
        
        return HttpResponse(f"Производительность протестирована. Найдено лошадей: {count}")


def test_sentry_user_context(request: HttpRequest) -> HttpResponse:
    """
    Тестовое представление для проверки контекста пользователя в Sentry.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Ответ с информацией о контексте пользователя
    """
    import sentry_sdk
    
    sentry_sdk.set_user({
        "id": request.user.id if request.user.is_authenticated else None,
        "username": request.user.username if request.user.is_authenticated else "anonymous",
        "email": request.user.email if request.user.is_authenticated else None,
    })
    
    sentry_sdk.set_context("request_info", {
        "method": request.method,
        "path": request.path,
        "user_agent": request.META.get('HTTP_USER_AGENT', ''),
    })
    
    return HttpResponse("Контекст пользователя установлен в Sentry")


# Django Silk Test Views
@silk_profile(name='test_silk_slow_query')
def test_silk_slow_query(request: HttpRequest) -> HttpResponse:
    """
    Тестовое представление для демонстрации медленных запросов в Silk.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Ответ с информацией о выполненных запросах
    """
    import time
    
    # Имитация медленного запроса
    time.sleep(0.5)
    
    # Выполнение нескольких запросов к БД
    horses = Horse.objects.all()
    trainers = Trainer.objects.all()
    news = NewsPost.objects.all()
    
    # Еще одна имитация медленного запроса
    time.sleep(0.3)
    
    context = {
        'horses_count': horses.count(),
        'trainers_count': trainers.count(),
        'news_count': news.count(),
        'message': 'Silk профилирование работает!'
    }
    
    return HttpResponse(f"Silk профилирование работает! Лошадей: {context['horses_count']}, Тренеров: {context['trainers_count']}, Новостей: {context['news_count']}")


@silk_profile(name='test_silk_memory_usage')
def test_silk_memory_usage(request: HttpRequest) -> HttpResponse:
    """
    Тестовое представление для демонстрации профилирования памяти в Silk.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Ответ с информацией об использовании памяти
    """
    import gc
    
    # Создание большого количества объектов для тестирования памяти
    large_list = []
    for i in range(10000):
        large_list.append(f"item_{i}")
    
    # Выполнение операций с данными
    horses = list(Horse.objects.all())
    trainers = list(Trainer.objects.all())
    
    # Очистка памяти
    del large_list
    gc.collect()
    
    return HttpResponse(f"Профилирование памяти завершено! Обработано лошадей: {len(horses)}, тренеров: {len(trainers)}")


@silk_profile(name='test_silk_database_queries')
def test_silk_database_queries(request: HttpRequest) -> HttpResponse:
    """
    Тестовое представление для демонстрации профилирования SQL запросов в Silk.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Ответ с результатами запросов
    """
    from django.db import connection
    
    # Выполнение различных типов запросов
    horses = Horse.objects.select_related('trainer').all()
    trainers_with_horses = Trainer.objects.prefetch_related('horses').all()
    news_with_attachments = NewsPost.objects.filter(attachment__isnull=False)
    
    # Сложный запрос с агрегацией
    horse_stats = Horse.objects.aggregate(
        total_count=Count('id'),
        avg_age=Avg('age'),
        max_age=Max('age')
    )
    
    # Запрос с фильтрацией
    young_horses = Horse.objects.filter(age__lt=5)
    experienced_trainers = Trainer.objects.filter(experience_years__gte=10)
    
    return HttpResponse(
        f"SQL запросы профилированы! "
        f"Лошадей: {len(list(horses[:3]))}, "
        f"Тренеров: {len(list(trainers_with_horses[:3]))}, "
        f"Новостей с вложениями: {news_with_attachments.count()}, "
        f"Молодых лошадей: {young_horses.count()}, "
        f"Опытных тренеров: {experienced_trainers.count()}"
    ) 