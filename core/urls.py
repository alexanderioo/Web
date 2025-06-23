from rest_framework.routers import DefaultRouter
from .views import AfExamViewSet

router = DefaultRouter()
router.register(r'afexam', AfExamViewSet, basename='afexam')

urlpatterns = router.urls 