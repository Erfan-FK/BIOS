from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views._tour_report_view import TourReportViewSet

router = DefaultRouter()
router.register('tour_report', TourReportViewSet)

urlpatterns = router.urls
