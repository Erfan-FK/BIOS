from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views._reg_request_view import RegRequestViewSet

router = DefaultRouter()
router.register('reg_request', RegRequestViewSet)

urlpatterns = router.urls  