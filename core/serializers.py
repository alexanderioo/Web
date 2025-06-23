from rest_framework import serializers
from .models import NewsPost, Trainer, Horse, UserProfile, User, Lesson, Payment, AfExam
from typing import Optional

class NewsPostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для новости.
    """
    author_name = serializers.CharField(source='author.user.username', read_only=True)

    class Meta:
        model = NewsPost
        fields = [
            'id', 'title', 'title_en', 'content', 'image', 'created_at', 
            'published_at', 'is_active', 'is_scheduled', 'attachment', 'author_name'
        ]

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
    full_name_en = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = [
            'id', 'full_name', 'full_name_en', 'first_name', 'first_name_en', 
            'last_name', 'last_name_en', 'bio', 'photo', 
            'experience_years', 'lessons_count', 'is_top_trainer'
        ]

    def get_is_top_trainer(self, obj: Trainer) -> bool:
        """
        Проверяет, является ли тренер "топовым" на основе данных из контекста.
        """
        top_trainer_ids = self.context.get('top_trainer_ids', [])
        return obj.id in top_trainer_ids

    def get_full_name_en(self, obj: Trainer) -> str:
        """
        Возвращает полное имя тренера на английском языке.
        """
        if obj.first_name_en and obj.last_name_en:
            return f"{obj.first_name_en} {obj.last_name_en}"
        elif obj.first_name_en:
            return f"{obj.first_name_en} {obj.last_name}"
        elif obj.last_name_en:
            return f"{obj.first_name} {obj.last_name_en}"
        else:
            return f"{obj.first_name} {obj.last_name}"

class HorseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для лошади.
    """
    trainer_names = serializers.SerializerMethodField()

    class Meta:
        model = Horse
        fields = [
            'id', 'name', 'name_en', 'birth_date', 'gender', 'photo', 
            'description', 'stable', 'trainer_names'
        ]

    def get_trainer_names(self, obj: Horse) -> list[str]:
        """
        Возвращает список имен тренеров лошади.
        """
        return [f"{trainer.first_name} {trainer.last_name}" for trainer in obj.trainers.all()]

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

class AfExamSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(many=True, read_only=True, slug_field='email')
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = AfExam
        fields = ['id', 'title', 'created_at', 'date', 'image', 'users', 'is_public']