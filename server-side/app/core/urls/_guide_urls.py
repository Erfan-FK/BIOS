from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views._guide_view import GuideViewSet

router = DefaultRouter()
router.register('guide', GuideViewSet)

urlpatterns = router.urls
