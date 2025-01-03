from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from core.auth.serializers import AuthSerializer, CurrentUserSerializer, UserRegisterSerializer, UserRegistrationResponseSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password

class LoginView(TokenObtainPairView):
    """
    Custom Login View using AuthSerializer for JWT.
    """
    serializer_class = AuthSerializer
    permission_classes = [AllowAny]


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=CurrentUserSerializer)
    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "profilePicture": user.profile_picture,
        }

        # If user is a guide, add guide's id
        if user.role == "guide" and hasattr(user, 'guide_profile'):
            data["profile_id"] = user.guide_profile.id

        # If user is an advisor, add advisor's id
        if user.role == "advisor" or user.role == "coordinator" and hasattr(user, 'advisor_profile'):
            data["profile_id"] = user.advisor_profile.id
            
        # If user is an advisor, add advisor's id
        if user.role == "visitor" and hasattr(user, 'visitor_profile'):
            data["profile_id"] = user.visitor_profile.id

        return Response(data)

class RegisterView(CreateAPIView):
    """
    View for user registration.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegisterSerializer,
        responses={
            201: OpenApiResponse(UserRegistrationResponseSerializer, description="User registered successfully"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ChangePasswordView(APIView):
    """
    View for authenticated users to change their password.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        # Validate current password
        if not user.check_password(current_password):
            return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Update to the new password
        user.password = make_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
