from rest_framework import serializers
from .models import NewsPost, Trainer, Horse, UserProfile, User, Lesson, Payment
from typing import Optional

class NewsPostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NewsPost.
    """
    class Meta:
        model = NewsPost
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для стандартного пользователя Django.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя.
    """
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user']

class TrainerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тренера.
    Демонстрирует использование SerializerMethodField и контекста.
    """
    lessons_count = serializers.IntegerField(read_only=True)
    is_top_trainer = serializers.SerializerMethodField()
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = Trainer
        fields = [
            'id', 'full_name', 'first_name', 'last_name', 'bio', 'photo', 
            'experience_years', 'lessons_count', 'is_top_trainer'
        ]

    def get_is_top_trainer(self, obj: Trainer) -> bool:
        """
        Проверяет, является ли тренер "топовым" на основе данных из контекста.
        """
        top_trainer_ids = self.context.get('top_trainer_ids', [])
        return obj.id in top_trainer_ids

class HorseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для лошади с использованием SerializerMethodField.
    """
    trainer_name = serializers.SerializerMethodField()
    lessons_this_month = serializers.SerializerMethodField()

    class Meta:
        model = Horse
        fields = [
            'id', 'name', 'gender', 'photo', 'description',
            'trainer_name', 'lessons_this_month'
        ]

    def get_trainer_name(self, obj: Horse) -> Optional[str]:
        """
        Возвращает полное имя тренера, если он назначен.
        Если тренеров несколько, возвращает их имена через запятую.
        """
        trainers = obj.trainers.all()
        if not trainers:
            return None
        
        trainer_names = [t.get_full_name() for t in trainers]
        return ", ".join(trainer_names)

    def get_lessons_this_month(self, obj: Horse) -> int:
        """
        Возвращает количество занятий у лошади в текущем месяце.
        """
        from django.utils import timezone
        now = timezone.now()
        return obj.lessons.filter(date__year=now.year, date__month=now.month).count()

class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для занятия (урока).
    """
    horse_name = serializers.SerializerMethodField()
    trainer_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    is_expensive = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'horse', 'horse_name', 'trainer', 'trainer_name',
            'student', 'student_name', 'date', 'price', 'status', 'is_expensive'
        ]

    def get_horse_name(self, obj: Lesson) -> str:
        return obj.horse.name

    def get_trainer_name(self, obj: Lesson) -> str:
        return obj.trainer.get_full_name()

    def get_student_name(self, obj: Lesson) -> str:
        return obj.student.user.username

    def get_is_expensive(self, obj: Lesson) -> bool:
        """
        Возвращает True, если цена урока выше средней.
        Средняя цена передается через контекст.
        """
        average_price = self.context.get('average_price', 0)
        if average_price > 0 and obj.price is not None:
            return obj.price > average_price
        return False

class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для платежа.
    """
    user_name: serializers.CharField = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_name', 'lesson', 'amount', 'timestamp', 'status', 'purpose', 'reference_id']