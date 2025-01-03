from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views._fair_view import FairViewSet

router = DefaultRouter()
router.register('fair', FairViewSet)

urlpatterns = router.urls
