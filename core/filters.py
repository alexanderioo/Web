import django_filters
from django_filters import DateFilter, CharFilter, ChoiceFilter, NumberFilter
from .models import NewsPost, Trainer, Horse, Lesson, Payment


class NewsPostFilter(django_filters.FilterSet):
    """
    Фильтр для модели NewsPost.
    Позволяет фильтровать по заголовку, контенту, дате публикации и активности.
    """
    title: CharFilter = CharFilter(lookup_expr='icontains', label='Заголовок содержит')
    content: CharFilter = CharFilter(lookup_expr='icontains', label='Контент содержит')
    published_after: DateFilter = DateFilter(field_name='published_at', lookup_expr='gte', label='Опубликовано после')
    published_before: DateFilter = DateFilter(field_name='published_at', lookup_expr='lte', label='Опубликовано до')
    is_active: ChoiceFilter = ChoiceFilter(choices=[(True, 'Активные'), (False, 'Неактивные')], label='Статус')
    
    class Meta:
        model = NewsPost
        fields = {
            'created_at': ['gte', 'lte'],
        }


class TrainerFilter(django_filters.FilterSet):
    """
    Фильтр для модели Trainer.
    Позволяет фильтровать по имени, фамилии, биографии и опыту.
    """
    first_name: CharFilter = CharFilter(lookup_expr='icontains', label='Имя содержит')
    last_name: CharFilter = CharFilter(lookup_expr='icontains', label='Фамилия содержит')
    bio: CharFilter = CharFilter(lookup_expr='icontains', label='Биография содержит')
    experience_min: NumberFilter = NumberFilter(field_name='experience_years', lookup_expr='gte', label='Опыт от (лет)')
    experience_max: NumberFilter = NumberFilter(field_name='experience_years', lookup_expr='lte', label='Опыт до (лет)')
    
    class Meta:
        model = Trainer
        fields = ['first_name', 'last_name', 'bio', 'experience_years']


class HorseFilter(django_filters.FilterSet):
    """
    Фильтр для модели Horse.
    Позволяет фильтровать по имени, описанию, полу и конюшне.
    """
    name: CharFilter = CharFilter(lookup_expr='icontains', label='Имя содержит')
    description: CharFilter = CharFilter(lookup_expr='icontains', label='Описание содержит')
    gender: ChoiceFilter = ChoiceFilter(choices=Horse.GENDER_CHOICES, label='Пол')
    stable: django_filters.ModelChoiceFilter = django_filters.ModelChoiceFilter(queryset=Horse.objects.values_list('stable__name', flat=True).distinct(), label='Конюшня')
    
    class Meta:
        model = Horse
        fields = {
            'birth_date': ['gte', 'lte'],
        }


class LessonFilter(django_filters.FilterSet):
    """
    Фильтр для модели Lesson.
    Позволяет фильтровать по ученику, тренеру, лошади, дате, цене и статусу.
    """
    student_name: CharFilter = CharFilter(field_name='student__user__username', lookup_expr='icontains', label='Ученик')
    trainer_name: CharFilter = CharFilter(field_name='trainer__first_name', lookup_expr='icontains', label='Имя тренера')
    horse_name: CharFilter = CharFilter(field_name='horse__name', lookup_expr='icontains', label='Лошадь')
    date_after: DateFilter = DateFilter(field_name='date', lookup_expr='gte', label='Дата после')
    date_before: DateFilter = DateFilter(field_name='date', lookup_expr='lte', label='Дата до')
    price_min: NumberFilter = NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    price_max: NumberFilter = NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')
    status: ChoiceFilter = ChoiceFilter(choices=Lesson.STATUS_CHOICES, label='Статус')
    
    class Meta:
        model = Lesson
        fields = {
            'date': ['gte', 'lte'],
            'price': ['gte', 'lte'],
        }


class PaymentFilter(django_filters.FilterSet):
    """
    Фильтр для модели Payment.
    Позволяет фильтровать по пользователю, назначению, сумме, дате и статусу.
    """
    user_name: CharFilter = CharFilter(field_name='user__username', lookup_expr='icontains', label='Пользователь')
    purpose: CharFilter = CharFilter(lookup_expr='icontains', label='Назначение содержит')
    amount_min: NumberFilter = NumberFilter(field_name='amount', lookup_expr='gte', label='Сумма от')
    amount_max: NumberFilter = NumberFilter(field_name='amount', lookup_expr='lte', label='Сумма до')
    timestamp_after: DateFilter = DateFilter(field_name='timestamp', lookup_expr='gte', label='Дата после')
    timestamp_before: DateFilter = DateFilter(field_name='timestamp', lookup_expr='lte', label='Дата до')
    status: ChoiceFilter = ChoiceFilter(choices=Payment.STATUS_CHOICES, label='Статус')
    
    class Meta:
        model = Payment
        fields = {
            'amount': ['gte', 'lte'],
            'timestamp': ['gte', 'lte'],
        } 