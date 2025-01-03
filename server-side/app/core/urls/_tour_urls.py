from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views._tour_view import TourViewSet

router = DefaultRouter()
router.register('tour', TourViewSet)

urlpatterns = router.urls
