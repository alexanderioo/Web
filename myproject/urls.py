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
    
    # Sentry Test URLs
    path('sentry/test-error/', views.test_sentry_error, name='sentry_test_error'),
    path('sentry/test-performance/', views.test_sentry_performance, name='sentry_test_performance'),
    path('sentry/test-user-context/', views.test_sentry_user_context, name='sentry_test_user_context'),
    
    # Django Silk Test URLs
    path('silk/test-slow-query/', views.test_silk_slow_query, name='silk_test_slow_query'),
    path('silk/test-memory-usage/', views.test_silk_memory_usage, name='silk_test_memory_usage'),
    path('silk/test-database-queries/', views.test_silk_database_queries, name='silk_test_database_queries'),
    
    # Django Silk URLs
    path('silk/', include('silk.urls', namespace='silk')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)