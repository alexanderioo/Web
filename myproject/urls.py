from django.contrib import admin
from django.urls import path, include
from core import views
from rest_framework import routers
from core.views import NewsPostViewSet, TrainerViewSet, HorseViewSet, LessonViewSet, PaymentViewSet
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'news', NewsPostViewSet)
router.register(r'trainers', TrainerViewSet)
router.register(r'horses', HorseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # API URLs
    path('api/news/', views.NewsPostViewSet.as_view({'get': 'list'}), name='api_news_list'),
    path('api/trainers/', views.TrainerViewSet.as_view({'get': 'list'}), name='api_trainers_list'),
    path('api/horses/', views.HorseViewSet.as_view({'get': 'list'}), name='api_horses_list'),
    path('api/lessons/', views.LessonViewSet.as_view({'get': 'list'}), name='api_lessons_list'),
    path('api/payments/', views.PaymentViewSet.as_view({'get': 'list'}), name='api_payments_list'),
    
    # Django Allauth URLs
    path('accounts/', include('allauth.urls')),
    
    # Sentry Test URLs
    path('sentry/test-error/', views.test_sentry_error, name='sentry_test_error'),
    path('sentry/test-performance/', views.test_sentry_performance, name='sentry_test_performance'),
    path('sentry/test-user-context/', views.test_sentry_user_context, name='sentry_test_user_context'),
    
    # Django Silk Test URLs
    path('silk/test-slow-query/', views.test_silk_slow_query, name='silk_test_slow_query'),
    path('silk/test-memory-usage/', views.test_silk_memory_usage, name='silk_test_memory_usage'),
    path('silk/test-database-queries/', views.test_silk_database_queries, name='silk_test_database_queries'),
    
    # Email Test URL
    path('test-email/', views.test_email_sending, name='test_email_sending'),
    
    # Django Silk URLs
    path('silk/', include('silk.urls', namespace='silk')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)