from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views._tour_request_view import TourRequestViewSet

router = DefaultRouter()
router.register('tour_request', TourRequestViewSet)

urlpatterns = router.urls
