from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views._tour_request_batch_view import TourRequestBatchViewSet

router = DefaultRouter()
router.register('tour_request_batch', TourRequestBatchViewSet)

urlpatterns = router.urls
