from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views._advisor_view import AdvisorViewSet

router = DefaultRouter()
router.register('advisor', AdvisorViewSet)

urlpatterns = router.urls
