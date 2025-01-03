from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views._visitor_view import VisitorViewSet

router = DefaultRouter()
router.register('visitor', VisitorViewSet)

urlpatterns = router.urls
