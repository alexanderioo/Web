from typing import Optional
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, EmailValidator


class Stable(models.Model):
    """
    Модель конюшни.
    Хранит информацию о названии, местоположении и вместимости конюшни.
    """
    name = models.CharField(
        "Название", 
        max_length=100,
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z0-9\s\-\.]+$', 
                'Название может содержать только буквы, цифры, пробелы, дефисы и точки'
            )
        ]
    )
    location = models.CharField(
        "Местоположение", 
        max_length=200,
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z0-9\s\-\.\,]+$', 
                'Местоположение может содержать только буквы, цифры, пробелы, дефисы, точки и запятые'
            )
        ]
    )
    capacity = models.PositiveIntegerField(
        "Вместимость",
        validators=[
            MinValueValidator(1, 'Вместимость должна быть не менее 1'),
            MaxValueValidator(1000, 'Вместимость не может превышать 1000')
        ]
    )

    class Meta:
        verbose_name = "Конюшня"
        verbose_name_plural = "Конюшни"
        ordering = ["name"]

    def __str__(self) -> str:
        """
        Возвращает строковое представление конюшни (название).
        """
        return self.name


class UserProfile(models.Model):
    """
    Профиль пользователя, расширяющий стандартную модель User.
    Содержит телефон, адрес и флаг тренера.
    """
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(
        "Телефон", 
        max_length=20,
        validators=[
            RegexValidator(
                r'^\+?[0-9\s\-\(\)]+$', 
                'Телефон может содержать только цифры, пробелы, дефисы, скобки и знак +'
            )
        ]
    )
    address = models.CharField(
        "Адрес", 
        max_length=255, 
        blank=True,
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z0-9\s\-\.\,]+$', 
                'Адрес может содержать только буквы, цифры, пробелы, дефисы, точки и запятые'
            )
        ]
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self) -> str:
        """
        Возвращает строковое представление профиля (имя пользователя).
        """
        return self.user.username


class Trainer(models.Model):
    """
    Модель тренера.
    Содержит имя, фото, опыт и биографию.
    """
    first_name = models.CharField(
        "Имя", 
        max_length=100,
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z\s]+$', 
                'Имя может содержать только буквы и пробелы'
            )
        ]
    )
    first_name_en = models.CharField(
        "Имя (англ.)", 
        max_length=100,
        blank=True,
        validators=[
            RegexValidator(
                r'^[a-zA-Z\s]+$', 
                'Английское имя может содержать только латинские буквы и пробелы'
            )
        ]
    )
    last_name = models.CharField(
        "Фамилия", 
        max_length=100,
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z\s]+$', 
                'Фамилия может содержать только буквы и пробелы'
            )
        ]
    )
    last_name_en = models.CharField(
        "Фамилия (англ.)", 
        max_length=100,
        blank=True,
        validators=[
            RegexValidator(
                r'^[a-zA-Z\s]+$', 
                'Английская фамилия может содержать только латинские буквы и пробелы'
            )
        ]
    )
    bio = models.TextField(
        "О себе",
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z0-9\s\-\.\,!?]+$', 
                'Биография может содержать только буквы, цифры, пробелы, дефисы, точки, запятые, восклицательные и вопросительные знаки'
            )
        ]
    )
    photo = models.ImageField("Фото", upload_to='trainers/', blank=True, null=True)
    experience_years = models.PositiveIntegerField(
        "Опыт (лет)",
        validators=[
            MinValueValidator(0, 'Опыт не может быть отрицательным'),
            MaxValueValidator(50, 'Опыт не может превышать 50 лет')
        ]
    )

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        """
        Возвращает строковое представление тренера (полное имя).
        """
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self) -> str:
        """
        Возвращает полное имя тренера.
        """
        return f"{self.first_name} {self.last_name}"


class Horse(models.Model):
    """
    Модель лошади.
    Содержит имя, дату рождения, пол, фото, описание, конюшню и тренеров.
    """
    GENDER_CHOICES = [
        ('male', 'Жеребец'),
        ('female', 'Кобыла'),
    ]

    name = models.CharField(
        "Имя", 
        max_length=100,
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z0-9\s\-]+$', 
                'Имя лошади может содержать только буквы, цифры, пробелы и дефисы'
            )
        ]
    )
    name_en = models.CharField(
        "Имя (англ.)", 
        max_length=100,
        blank=True,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9\s\-]+$', 
                'Английское имя может содержать только латинские буквы, цифры, пробелы и дефисы'
            )
        ]
    )
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    gender = models.CharField("Пол", max_length=10, choices=GENDER_CHOICES)
    
    photo = models.ImageField("Фото", upload_to='horses/', blank=True, null=True)
    description = models.TextField(
        "Описание", 
        blank=True, 
        null=True,
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z0-9\s\-\.\,!?]+$', 
                'Описание может содержать только буквы, цифры, пробелы, дефисы, точки, запятые, восклицательные и вопросительные знаки'
            )
        ]
    )

    stable = models.ForeignKey(
        Stable,
        verbose_name="Конюшня",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="horses"
    )

    trainers = models.ManyToManyField(
        'Trainer',
        through='HorseTrainerRelation',
        through_fields=('horse', 'trainer'),
        verbose_name="Тренеры",
        related_name="horses",
        blank=True
    )

    class Meta:
        verbose_name = "Лошадь"
        verbose_name_plural = "Лошади"
        ordering = ["name"]

    def __str__(self) -> str:
        """
        Возвращает строковое представление лошади (имя).
        """
        return self.name

class HorseTrainerRelation(models.Model):
    """
    Промежуточная модель для связи лошади и тренера.
    Хранит дату начала работы и заметки.
    """
    horse = models.ForeignKey("Horse", on_delete=models.CASCADE)
    trainer = models.ForeignKey("Trainer", on_delete=models.CASCADE)
    start_date = models.DateField("Дата начала работы")
    notes = models.TextField(
        "Заметки", 
        blank=True,
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z0-9\s\-\.\,!?]+$', 
                'Заметки могут содержать только буквы, цифры, пробелы, дефисы, точки, запятые, восклицательные и вопросительные знаки'
            )
        ]
    )

    class Meta:
        verbose_name = "Связь Лошади и Тренера"
        verbose_name_plural = "Связи Лошадей и Тренеров"
        unique_together = ('horse', 'trainer')

    def __str__(self) -> str:
        """
        Возвращает строковое представление связи лошади и тренера.
        """
        return f"{self.trainer} ↔ {self.horse} с {self.start_date}"


class CompletedLessonManager(models.Manager):
    """
    Кастомный менеджер для получения завершённых занятий.
    """
    def get_queryset(self) -> models.QuerySet:
        """
        Возвращает QuerySet только завершённых занятий.
        """
        return super().get_queryset().filter(status='completed')


class Lesson(models.Model):
    """
    Модель занятия (урока).
    Содержит лошадь, тренера, ученика, дату, цену и статус.
    """
    STATUS_CHOICES = [
        ('scheduled', 'Запланировано'),
        ('completed', 'Завершено'),
    ]

    horse = models.ForeignKey(Horse, verbose_name="Лошадь", on_delete=models.CASCADE, related_name="lessons")
    trainer = models.ForeignKey(Trainer, verbose_name="Тренер", on_delete=models.CASCADE, related_name="lessons")
    student = models.ForeignKey(UserProfile, verbose_name="Ученик", on_delete=models.CASCADE, related_name="lessons")
    date = models.DateTimeField("Дата и время занятия")
    price = models.DecimalField(
        "Цена", 
        max_digits=8, 
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, 'Цена должна быть больше 0'),
            MaxValueValidator(999999.99, 'Цена не может превышать 999999.99')
        ]
    )
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES)

    objects = models.Manager()
    completed = CompletedLessonManager()

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"
        ordering = ['-date']

    def __str__(self) -> str:
        """
        Возвращает строковое представление занятия (имя ученика и дата).
        """
        return f"{self.student.user.username} - {self.date}"


class Payment(models.Model):
    """
    Модель платежа за занятие.
    Содержит пользователя, занятие, сумму, дату, статус, назначение и ID транзакции.
    """
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('completed', 'Завершено'),
        ('failed', 'Неудачно'),
    ]

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="payments")
    lesson = models.OneToOneField(
        Lesson,
        verbose_name="Занятие",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payment"
    )
    amount = models.DecimalField(
        "Сумма", 
        max_digits=10, 
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, 'Сумма должна быть больше 0'),
            MaxValueValidator(99999999.99, 'Сумма не может превышать 99999999.99')
        ]
    )
    timestamp = models.DateTimeField("Дата и время", default=timezone.now)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES)
    purpose = models.CharField(
        "Назначение", 
        max_length=100,
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z0-9\s\-\.\,]+$', 
                'Назначение может содержать только буквы, цифры, пробелы, дефисы, точки и запятые'
            )
        ]
    )
    reference_id = models.CharField(
        "ID транзакции", 
        max_length=100, 
        blank=True, 
        null=True,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9\-_]+$', 
                'ID транзакции может содержать только буквы, цифры, дефисы и подчеркивания'
            )
        ]
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
        ordering = ['-timestamp']

    def __str__(self) -> str:
        """
        Возвращает строковое представление платежа (пользователь, сумма, статус).
        """
        return f"{self.user.username} - {self.amount} - {self.status}"


class NewsPost(models.Model):
    """
    Модель новости.
    Содержит заголовок, контент, изображение, дату создания, публикации, статус и автора.
    """
    title = models.CharField(
        "Заголовок", 
        max_length=200,
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z0-9\s\-\.\,!?]+$', 
                'Заголовок может содержать только буквы, цифры, пробелы, дефисы, точки, запятые, восклицательные и вопросительные знаки'
            )
        ]
    )
    title_en = models.CharField(
        "Заголовок (англ.)", 
        max_length=200,
        blank=True,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9\s\-\.\,!?]+$', 
                'Английский заголовок может содержать только латинские буквы, цифры, пробелы, дефисы, точки, запятые, восклицательные и вопросительные знаки'
            )
        ]
    )
    content = models.TextField(
        "Контент",
        validators=[
            RegexValidator(
                r'^[а-яА-Яa-zA-Z0-9\s\-\.\,!?<>/]+$', 
                'Контент может содержать только буквы, цифры, пробелы, дефисы, точки, запятые, восклицательные и вопросительные знаки, а также HTML теги'
            )
        ]
    )
    image = models.ImageField("Изображение", upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField("Создано", default=timezone.now)
    published_at = models.DateTimeField("Дата публикации", null=True, blank=True)
    is_active = models.BooleanField("Активна", default=True)
    is_scheduled = models.BooleanField("Запланирована", default=False)
    attachment = models.FileField("Вложение", upload_to='news_attachments/', blank=True, null=True)

    author = models.ForeignKey(
        UserProfile,
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_posts"
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self) -> str:
        """
        Возвращает строковое представление новости (заголовок).
        """
        return self.title

    def get_absolute_url(self) -> str:
        """
        Возвращает абсолютный URL для просмотра новости.
        """
        return reverse("news_detail", args=[str(self.id)])


class ScheduleRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(UserProfile, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="schedule_requests")
    preferred_time = models.DateTimeField("Предпочтительное время")
    horse = models.ForeignKey(Horse, verbose_name="Лошадь", on_delete=models.SET_NULL, null=True, blank=True, related_name="schedule_requests")
    trainer = models.ForeignKey(Trainer, verbose_name="Тренер", on_delete=models.SET_NULL, null=True, blank=True, related_name="schedule_requests")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = "Запрос на расписание"
        verbose_name_plural = "Запросы на расписание"
        ordering = ["-preferred_time"]

    def __str__(self):
        return f"{self.user.user.username} - {self.preferred_time}"

class Resource(models.Model):
    title = models.CharField("Название", max_length=200)
    link = models.URLField("Ссылка", blank=True)

    def __str__(self):
        return self.title