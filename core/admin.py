from typing import Any
from django.contrib import admin
from .models import (
    Horse,
    Trainer,
    UserProfile,
    Lesson,
    NewsPost,
    Stable,
    ScheduleRequest,
    Payment,
    HorseTrainerRelation,
    Resource,
    AfExam
)
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO

@admin.action(description="Скачать PDF со списком новостей")
def export_news_to_pdf(modeladmin: admin.ModelAdmin, request: Any, queryset: Any) -> HttpResponse:
    """
    Экспорт выбранных новостей в PDF-файл.
    """
    from reportlab.pdfgen import canvas
    from io import BytesIO
    from django.http import HttpResponse

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    y = 800

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, y, "Список новостей")
    y -= 40

    for post in queryset:
        p.setFont("Helvetica", 12)
        text = f"{post.title} — {post.published_at.strftime('%d.%m.%Y %H:%M') if post.published_at else 'Не опубликовано'}"
        p.drawString(100, y, text)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

@admin.register(Horse)
class HorseAdmin(admin.ModelAdmin):
    """
    Админка для модели Horse.
    """
    list_display = ("name", "gender", "birth_date", "stable")
    list_filter = ("gender", "stable")
    search_fields = ("name", "gender", "stable__name", "trainers__profile__user__username")
    raw_id_fields = ("stable",)


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    """
    Админка для модели Trainer.
    """
    list_display = ("first_name", "last_name", "experience_years")
    search_fields = ("first_name", "last_name", "bio")
    list_filter = ("experience_years",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Админка для профиля пользователя.
    """
    list_display = ("user", "phone")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "phone",
        "address"
    )
    list_filter = ()
    raw_id_fields = ("user",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Админка для модели Lesson.
    """
    list_display = ("date", "student_name", "trainer", "horse", "status", "price")
    list_filter = ("status", "trainer", "horse")
    search_fields = (
        "student__user__username",
        "student__user__first_name",
        "trainer__first_name",
        "trainer__last_name",
        "horse__name"
    )
    raw_id_fields = ("student", "trainer", "horse")
    date_hierarchy = "date"

    @admin.display(description="Ученик")
    def student_name(self, obj: Lesson) -> str:
        """
        Возвращает имя пользователя-ученика.
        """
        return obj.student.user.username


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Админка для модели Payment.
    """
    list_display = ("user_name", "lesson", "amount", "status", "timestamp", "reference_display")
    list_filter = ("status",)
    search_fields = (
        "user__username",
        "user__first_name",
        "lesson__id",
        "reference_id",
        "purpose"
    )
    raw_id_fields = ("lesson", "user")
    date_hierarchy = "timestamp"

    @admin.display(description="Пользователь")
    def user_name(self, obj: Payment) -> str:
        """
        Возвращает имя пользователя, совершившего платёж.
        """
        return obj.user.username if obj.user else "—"

    @admin.display(description="ID транзакции")
    def reference_display(self, obj: Payment) -> str:
        """
        Возвращает ID транзакции или прочерк.
        """
        return obj.reference_id or "—"


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    """
    Админка для модели NewsPost.
    """
    list_display = ("title", "created_at", "published_at", "is_active", "is_scheduled")
    list_filter = ("is_active", "is_scheduled")
    search_fields = (
        "title",
        "content",
        "author__user__username"
    )
    date_hierarchy = "created_at"
    actions = [export_news_to_pdf]


@admin.register(Stable)
class StableAdmin(admin.ModelAdmin):
    """
    Админка для модели Stable.
    """
    list_display = ("name", "location", "capacity")
    search_fields = ("name", "location")


@admin.register(ScheduleRequest)
class ScheduleRequestAdmin(admin.ModelAdmin):
    """
    Админка для модели ScheduleRequest.
    """
    list_display = ("user", "preferred_time", "status", "trainer", "horse")
    list_filter = ("status",)
    search_fields = (
        "user__user__username",
        "horse__name",
        "trainer__first_name",
        "trainer__last_name",
    )
    raw_id_fields = ("user", "horse", "trainer")
    date_hierarchy = "preferred_time"


@admin.register(HorseTrainerRelation)
class HorseTrainerRelationAdmin(admin.ModelAdmin):
    """
    Админка для промежуточной модели HorseTrainerRelation.
    """
    list_display = ("horse", "trainer", "start_date", "notes")
    search_fields = (
        "horse__name",
        "trainer__first_name",
        "trainer__last_name",
        "notes"
    )
    raw_id_fields = ("horse", "trainer")
    date_hierarchy = "start_date"

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """
    Админка для модели Resource.
    """
    list_display = ("title", "link")

@admin.register(AfExam)
class AfExamAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "is_public", "created_at", "image_tag")
    list_filter = ("is_public", "created_at")
    search_fields = ("title", "users__email")
    filter_horizontal = ("users",)
    readonly_fields = ("created_at", "image_tag")
    date_hierarchy = "date"

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 60px; max-width: 100px;" />'
        return "—"
    image_tag.short_description = "Картинка"
    image_tag.allow_tags = True