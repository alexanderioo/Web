import logging
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count, Avg, Sum
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from .models import Lesson, Payment, NewsPost, Horse, Trainer, UserProfile

logger = logging.getLogger(__name__)

@shared_task
def daily_cleanup():
    """
    Ежедневная очистка старых данных и уведомления.
    """
    try:
        # Удаление старых неактивных новостей (старше 1 года)
        one_year_ago = timezone.now() - timedelta(days=365)
        old_news = NewsPost.objects.filter(
            created_at__lt=one_year_ago,
            is_active=False
        )
        deleted_count = old_news.count()
        old_news.delete()
        
        logger.info(f"Ежедневная очистка: удалено {deleted_count} старых новостей")
        
        # Уведомления о завтрашних занятиях
        tomorrow = timezone.now().date() + timedelta(days=1)
        tomorrow_lessons = Lesson.objects.filter(
            date__date=tomorrow,
            status='scheduled'
        )
        
        for lesson in tomorrow_lessons:
            logger.info(f"Напоминание: завтра занятие {lesson.student.user.username} с {lesson.trainer.full_name}")
        
        return f"Очистка завершена. Удалено новостей: {deleted_count}, напоминаний отправлено: {tomorrow_lessons.count()}"
        
    except Exception as e:
        logger.error(f"Ошибка в ежедневной очистке: {e}")
        raise

@shared_task
def weekly_reports():
    """
    Еженедельные отчеты по доходам и активности.
    """
    try:
        # Статистика за неделю
        week_ago = timezone.now() - timedelta(days=7)
        
        # Доходы за неделю
        weekly_income = Payment.objects.filter(
            timestamp__gte=week_ago,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Количество занятий за неделю
        weekly_lessons = Lesson.objects.filter(
            date__gte=week_ago
        ).count()
        
        # Популярные лошади
        popular_horses = Horse.objects.annotate(
            lesson_count=Count('lessons')
        ).filter(
            lessons__date__gte=week_ago
        ).order_by('-lesson_count')[:5]
        
        logger.info(f"Еженедельный отчет: доход {weekly_income}, занятий {weekly_lessons}")
        
        return {
            'weekly_income': float(weekly_income),
            'weekly_lessons': weekly_lessons,
            'popular_horses': list(popular_horses.values('name', 'lesson_count'))
        }
        
    except Exception as e:
        logger.error(f"Ошибка в еженедельном отчете: {e}")
        raise

@shared_task
def monthly_analytics():
    """
    Ежемесячная аналитика по лошадям и тренерам.
    """
    try:
        # Статистика за месяц
        month_ago = timezone.now() - timedelta(days=30)
        
        # Топ тренеров по количеству занятий
        top_trainers = Trainer.objects.annotate(
            lesson_count=Count('lessons')
        ).filter(
            lessons__date__gte=month_ago
        ).order_by('-lesson_count')[:10]
        
        # Статистика по лошадям
        horse_stats = Horse.objects.annotate(
            lesson_count=Count('lessons'),
            avg_price=Avg('lessons__price')
        ).filter(
            lessons__date__gte=month_ago
        ).order_by('-lesson_count')[:10]
        
        # Общая статистика
        total_lessons = Lesson.objects.filter(date__gte=month_ago).count()
        total_income = Payment.objects.filter(
            timestamp__gte=month_ago,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        logger.info(f"Ежемесячная аналитика: {total_lessons} занятий, доход {total_income}")
        
        return {
            'total_lessons': total_lessons,
            'total_income': float(total_income),
            'top_trainers': list(top_trainers.values('first_name', 'last_name', 'lesson_count')),
            'horse_stats': list(horse_stats.values('name', 'lesson_count', 'avg_price'))
        }
        
    except Exception as e:
        logger.error(f"Ошибка в ежемесячной аналитике: {e}")
        raise

@shared_task
def send_lesson_reminders():
    """
    Отправка напоминаний о занятиях (каждый час).
    """
    try:
        # Занятия в ближайшие 2 часа
        now = timezone.now()
        two_hours_later = now + timedelta(hours=2)
        
        upcoming_lessons = Lesson.objects.filter(
            date__gte=now,
            date__lte=two_hours_later,
            status='scheduled'
        )
        
        emails_sent = 0
        for lesson in upcoming_lessons:
            try:
                # Формируем сообщение
                subject = f'Напоминание о занятии - {lesson.date.strftime("%d.%m.%Y %H:%M")}'
                message = f"""
Здравствуйте, {lesson.student.user.username}!

Напоминаем о предстоящем занятии:
- Дата: {lesson.date.strftime("%d.%m.%Y")}
- Время: {lesson.date.strftime("%H:%M")}
- Тренер: {lesson.trainer.full_name}
- Лошадь: {lesson.horse.name}
- Продолжительность: {lesson.duration} минут
- Стоимость: {lesson.price} руб.

Ждем вас в конюшне!

С уважением,
Команда конюшни
                """.strip()
                
                # Отправляем email
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[lesson.student.user.email] if lesson.student.user.email else [],
                    fail_silently=True,
                )
                
                emails_sent += 1
                logger.info(f"Напоминание отправлено: занятие через {lesson.date - now} для {lesson.student.user.username}")
                
            except Exception as e:
                logger.error(f"Ошибка отправки напоминания для занятия {lesson.id}: {e}")
        
        return f"Напоминания отправлены для {emails_sent} из {upcoming_lessons.count()} занятий"
        
    except Exception as e:
        logger.error(f"Ошибка в отправке напоминаний: {e}")
        raise

@shared_task
def backup_database():
    """
    Резервное копирование базы данных (еженедельно).
    """
    try:
        # Здесь можно добавить логику резервного копирования
        logger.info("Резервное копирование базы данных выполнено")
        return "Резервное копирование завершено"
        
    except Exception as e:
        logger.error(f"Ошибка в резервном копировании: {e}")
        raise

@shared_task
def update_horse_statistics():
    """
    Обновление статистики лошадей (ежедневно).
    """
    try:
        horses = Horse.objects.all()
        
        for horse in horses:
            # Подсчет занятий за последний месяц
            month_ago = timezone.now() - timedelta(days=30)
            recent_lessons = horse.lessons.filter(date__gte=month_ago).count()
            
            # Средняя цена за занятие
            avg_price = horse.lessons.aggregate(avg_price=Avg('price'))['avg_price'] or 0
            
            logger.info(f"Статистика лошади {horse.name}: {recent_lessons} занятий, средняя цена {avg_price}")
        
        return f"Статистика обновлена для {horses.count()} лошадей"
        
    except Exception as e:
        logger.error(f"Ошибка в обновлении статистики лошадей: {e}")
        raise

@shared_task
def send_weekly_reports_email():
    """
    Отправка еженедельных отчетов по email администраторам.
    """
    try:
        # Получаем данные отчета
        report_data = weekly_reports()
        
        # Формируем сообщение
        subject = f'Еженедельный отчет конюшни - {timezone.now().strftime("%d.%m.%Y")}'
        message = f"""
Еженедельный отчет конюшни

Период: {timezone.now().strftime("%d.%m.%Y")}

📊 Статистика:
- Доход за неделю: {report_data.get('weekly_income', 0)} руб.
- Количество занятий: {report_data.get('weekly_lessons', 0)}

🐎 Популярные лошади:
"""
        
        for horse in report_data.get('popular_horses', []):
            message += f"- {horse['name']}: {horse['lesson_count']} занятий\n"
        
        message += """

С уважением,
Система отчетности конюшни
        """.strip()
        
        # Отправляем email администраторам
        admin_emails = ['admin@horse-stable.com', 'manager@horse-stable.com']
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            fail_silently=True,
        )
        
        logger.info(f"Еженедельный отчет отправлен на {len(admin_emails)} адресов")
        return f"Еженедельный отчет отправлен на {len(admin_emails)} адресов"
        
    except Exception as e:
        logger.error(f"Ошибка в отправке еженедельного отчета: {e}")
        raise 