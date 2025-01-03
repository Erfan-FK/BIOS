from rest_framework.routers import DefaultRouter
from core.views._user_views import UserViewSet, ProfilePictureView, ListUsersView
from django.urls import path

# Create a router and register viewsets
router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('user/update-profile-picture/', ProfilePictureView.as_view(), name='update-profile-picture'),
    path('users/list/', ListUsersView.as_view(), name='list-users'),
]

# Combine router and path URLs
urlpatterns += router.urls
