from rest_framework.permissions import BasePermission
from core.models._User import User

class IsGuide(BasePermission):
    """
    Permission for guides to access their own resources.
    """
    def has_permission(self, request, view):
        return has_role(request.user, ['guide'])

class IsAdvisor(BasePermission):
    """
    Permission for advisors to manage guides and tours.
    """
    def has_permission(self, request, view):
        return has_role(request.user, ['advisor', 'coordinator', 'director'])

class IsCoordinator(BasePermission):
    """
    Permission for coordinators to manage advisors and guides.
    """
    def has_permission(self, request, view):
        return has_role(request.user, ['coordinator', 'director'])

class IsDirector(BasePermission):
    """
    Permission for directors to access all resources.
    """
    def has_permission(self, request, view):
        return has_role(request.user, ['director'])

class IsOwnResource(BasePermission):
    """
    Permission to ensure a user can only access or modify their own data.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

def has_role(user, roles):
    """
    Check if the user's role is in the allowed roles.
    :param user: User object
    :param roles: List of allowed roles
    :return: Boolean
    """
    if not user.is_authenticated:
        return False
    return user.role in roles