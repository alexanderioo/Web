from typing import Any
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import (
    Stable, UserProfile, Trainer, Horse, Lesson, 
    Payment, NewsPost, ScheduleRequest, Resource
)
from .filters import NewsPostFilter, TrainerFilter, HorseFilter
from django_filters import rest_framework as filters


class ModelTests(TestCase):
    """
    Тесты для моделей данных (Stable, Horse, Trainer, Lesson, NewsPost).
    """
    
    def setUp(self) -> None:
        """
        Настройка тестовых данных для моделей.
        """
        # Создаем пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Иван',
            last_name='Иванов'
        )
        
        # Создаем профиль пользователя
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            phone='+7-999-123-45-67',
            address='ул. Тестовая, 1',
            is_trainer=False
        )
        
        # Создаем конюшню
        self.stable = Stable.objects.create(
            name='Тестовая конюшня',
            location='г. Москва',
            capacity=20
        )
        
        # Создаем тренера
        self.trainer_profile = UserProfile.objects.create(
            user=User.objects.create_user(
                username='trainer',
                password='trainer123',
                first_name='Александр',
                last_name='Петров'
            ),
            phone='+7-999-987-65-43',
            is_trainer=True
        )
        
        self.trainer = Trainer.objects.create(
            profile=self.trainer_profile,
            bio='Опытный тренер с 10-летним стажем',
            photo='trainers/test.jpg',
            experience_years=10
        )
        
        # Создаем лошадь
        self.horse = Horse.objects.create(
            name='Буран',
            gender='male',
            description='Спокойный и послушный конь',
            stable=self.stable
        )
        
        # Создаем новость
        self.news = NewsPost.objects.create(
            title='Тестовая новость',
            content='Содержание тестовой новости',
            is_active=True,
            published_at=timezone.now()
        )

    def test_stable_creation(self) -> None:
        """
        Тест 1: Создание конюшни.
        """
        stable = Stable.objects.create(
            name='Новая конюшня',
            location='г. Санкт-Петербург',
            capacity=15
        )
        self.assertEqual(stable.name, 'Новая конюшня')
        self.assertEqual(stable.capacity, 15)
        self.assertEqual(str(stable), 'Новая конюшня')

    def test_horse_creation(self) -> None:
        """
        Тест 2: Создание лошади.
        """
        horse = Horse.objects.create(
            name='Звездочка',
            gender='female',
            description='Красивая кобыла',
            stable=self.stable
        )
        self.assertEqual(horse.name, 'Звездочка')
        self.assertEqual(horse.gender, 'female')
        self.assertEqual(horse.stable, self.stable)

    def test_trainer_creation(self) -> None:
        """
        Тест 3: Создание тренера.
        """
        self.assertEqual(self.trainer.profile.user.first_name, 'Александр')
        self.assertEqual(self.trainer.experience_years, 10)
        self.assertTrue(self.trainer.profile.is_trainer)

    def test_lesson_creation(self) -> None:
        """
        Тест 4: Создание занятия.
        """
        lesson = Lesson.objects.create(
            horse=self.horse,
            trainer=self.trainer,
            student=self.user_profile,
            date=timezone.now() + timezone.timedelta(days=1),
            price=Decimal('1500.00'),
            status='scheduled'
        )
        self.assertEqual(lesson.horse, self.horse)
        self.assertEqual(lesson.trainer, self.trainer)
        self.assertEqual(lesson.price, Decimal('1500.00'))
        self.assertEqual(lesson.status, 'scheduled')

    def test_news_post_creation(self) -> None:
        """
        Тест 5: Создание новости.
        """
        news = NewsPost.objects.create(
            title='Важная новость',
            content='Очень важное содержание',
            is_active=True,
            published_at=timezone.now()
        )
        self.assertEqual(news.title, 'Важная новость')
        self.assertTrue(news.is_active)
        self.assertIsNotNone(news.published_at)


class APITests(APITestCase):
    """
    Тесты для API endpoints (news, trainers, horses, фильтрация, поиск).
    """
    
    def setUp(self) -> None:
        """
        Настройка тестовых данных для API.
        """
        # Создаем пользователя
        self.user = User.objects.create_user(
            username='apiuser',
            password='apipass123'
        )
        
        # Создаем профиль
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            phone='+7-999-111-22-33'
        )
        
        # Создаем тренера
        trainer_user = User.objects.create_user(
            username='apitrainer',
            password='trainerpass'
        )
        trainer_profile = UserProfile.objects.create(
            user=trainer_user,
            is_trainer=True
        )
        self.trainer = Trainer.objects.create(
            profile=trainer_profile,
            bio='API тестовый тренер',
            experience_years=5
        )
        
        # Создаем лошадь
        self.horse = Horse.objects.create(
            name='API Конь',
            gender='male',
            description='Тестовый конь для API'
        )
        
        # Создаем новости
        self.news1 = NewsPost.objects.create(
            title='API Новость 1',
            content='Содержание 1',
            is_active=True,
            published_at=timezone.now()
        )
        self.news2 = NewsPost.objects.create(
            title='API Новость 2',
            content='Содержание 2',
            is_active=False,
            published_at=timezone.now()
        )

    def test_trainers_list_api(self) -> None:
        """
        Тест 7: API список тренеров.
        """
        url = '/api/trainers/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_horses_list_api(self) -> None:
        """
        Тест 8: API список лошадей.
        """
        url = '/api/horses/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_news_filter_api(self) -> None:
        """
        Тест 9: API фильтрация новостей.
        """
        url = '/api/news/'
        response = self.client.get(url, {'title': 'API Новость 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'API Новость 1')

    def test_trainers_search_api(self) -> None:
        """
        Тест 10: API поиск тренеров.
        """
        url = '/api/trainers/'
        response = self.client.get(url, {'search': 'API тестовый'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class FilterTests(TestCase):
    """
    Тесты для фильтров Django Filter (NewsPost, Trainer, Horse).
    """
    
    def setUp(self) -> None:
        """
        Настройка тестовых данных для фильтров.
        """
        # Создаем пользователей и тренеров
        trainer_user = User.objects.create_user(
            username='filtertrainer',
            first_name='Фильтр',
            last_name='Тренеров'
        )
        trainer_profile = UserProfile.objects.create(
            user=trainer_user,
            is_trainer=True
        )
        self.trainer = Trainer.objects.create(
            profile=trainer_profile,
            bio='Тренер для тестирования фильтров',
            experience_years=8
        )
        
        # Создаем лошадей
        self.horse1 = Horse.objects.create(
            name='Фильтр Конь 1',
            gender='male',
            description='Первый конь для фильтров'
        )
        self.horse2 = Horse.objects.create(
            name='Фильтр Конь 2',
            gender='female',
            description='Второй конь для фильтров'
        )
        
        # Создаем новости
        self.news1 = NewsPost.objects.create(
            title='Фильтр Новость 1',
            content='Первая новость для фильтров',
            is_active=True,
            published_at=timezone.now()
        )
        self.news2 = NewsPost.objects.create(
            title='Фильтр Новость 2',
            content='Вторая новость для фильтров',
            is_active=False,
            published_at=timezone.now()
        )

    def test_news_filter_by_title(self) -> None:
        """
        Тест 11: Фильтр новостей по заголовку.
        """
        filter_set = NewsPostFilter({'title': 'Фильтр Новость 1'})
        self.assertTrue(filter_set.is_valid())
        queryset = filter_set.qs
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().title, 'Фильтр Новость 1')

    def test_news_filter_by_status(self) -> None:
        """
        Тест 12: Фильтр новостей по статусу.
        """
        filter_set = NewsPostFilter({'is_active': 'True'})
        self.assertTrue(filter_set.is_valid())
        queryset = filter_set.qs
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(queryset.first().is_active)

    def test_trainer_filter_by_experience(self) -> None:
        """
        Тест 13: Фильтр тренеров по опыту.
        """
        filter_set = TrainerFilter({'experience_min': '5'})
        self.assertTrue(filter_set.is_valid())
        queryset = filter_set.qs
        self.assertEqual(queryset.count(), 1)
        self.assertGreaterEqual(queryset.first().experience_years, 5)

    def test_horse_filter_by_gender(self) -> None:
        """
        Тест 14: Фильтр лошадей по полу.
        """
        filter_set = HorseFilter({'gender': 'male'})
        self.assertTrue(filter_set.is_valid())
        queryset = filter_set.qs
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().gender, 'male')

    def test_horse_filter_by_name(self) -> None:
        """
        Тест 15: Фильтр лошадей по имени.
        """
        filter_set = HorseFilter({'name': 'Фильтр Конь 1'})
        self.assertTrue(filter_set.is_valid())
        queryset = filter_set.qs
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().name, 'Фильтр Конь 1')


class IntegrationTests(TestCase):
    """
    Интеграционные тесты (админка, строковые представления, профиль, платежи).
    """
    
    def setUp(self) -> None:
        """
        Настройка для интеграционных тестов.
        """
        self.client = Client()
        
        # Создаем суперпользователя
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        
        # Создаем тестовые данные
        self.stable = Stable.objects.create(
            name='Интеграционная конюшня',
            location='г. Тест',
            capacity=10
        )
        
        self.horse = Horse.objects.create(
            name='Интеграционный конь',
            gender='male',
            stable=self.stable
        )

    def test_admin_access(self) -> None:
        """
        Тест 16: Доступ к админке.
        """
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_stable_str_representation(self) -> None:
        """
        Тест 17: Строковое представление конюшни.
        """
        self.assertEqual(str(self.stable), 'Интеграционная конюшня')

    def test_horse_str_representation(self) -> None:
        """
        Тест 18: Строковое представление лошади.
        """
        self.assertEqual(str(self.horse), 'Интеграционный конь')

    def test_user_profile_creation(self) -> None:
        """
        Тест 19: Создание профиля пользователя.
        """
        user = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        profile = UserProfile.objects.create(
            user=user,
            phone='+7-999-555-44-33',
            is_trainer=False
        )
        self.assertEqual(profile.user.username, 'testuser2')
        self.assertFalse(profile.is_trainer)

    def test_payment_creation(self) -> None:
        """
        Тест 20: Создание платежа.
        """
        user = User.objects.create_user(
            username='paymentuser',
            password='paymentpass'
        )
        payment = Payment.objects.create(
            user=user,
            amount=Decimal('2000.00'),
            purpose='Оплата занятий',
            status='completed'
        )
        self.assertEqual(payment.amount, Decimal('2000.00'))
        self.assertEqual(payment.purpose, 'Оплата занятий')
        self.assertEqual(payment.status, 'completed')
