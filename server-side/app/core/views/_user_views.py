from rest_framework.viewsets import ModelViewSet
from core.models._User import User
from core.serializers._user_serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from core.utils import send_email
from decouple import config
import cloudinary

class UserViewSet(ModelViewSet):
    """ViewSet for managing users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['post'], url_path='create-user') 
    def create_user(self, request):
        data = request.data
        # Generate a random plain-text password
        random_password = get_random_string(length=8)

        # Create the user
        user = User.objects.create_user(
            email=data['email'],
            name=data['name'],
            role=data['role'],
            password=random_password,  # Pass plain-text password here
        )

        profile_id = None

        if data['role'] == 'guide':
            guide = user.guide_profile
            guide.rating = 0
            guide.availability = [0 for _ in range(28)]
            guide.save()
            profile_id = guide.id  # Get guide profile ID
        elif data['role'] == 'advisor':
            advisor = user.advisor_profile
            advisor.save()
            profile_id = advisor.id  # Get advisor profile ID

        elif data['role'] == 'coordinator':
            advisor = user.advisor_profile
            advisor.save()
        # Send the plain-text password via email
        send_email(to_email=data['email'], receiver=data['name'], password=random_password)

        # Prepare the response data
        response_data = {
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role,
            },
        }

        # Include profile ID based on role
        if data['role'] == 'guide':
            response_data['guide_id'] = profile_id
        elif data['role'] == 'advisor':
            response_data['advisor_id'] = profile_id

        return Response(response_data, status=status.HTTP_201_CREATED)

class ProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        file = request.FILES.get("profile_picture")

        # Inline Cloudinary Configuration
        cloudinary.config(
            cloud_name=config("CLOUDINARY_CLOUD_NAME"),
            api_key=config("CLOUDINARY_API_KEY"),
            api_secret=config("CLOUDINARY_API_SECRET"),
            secure=True
        )
        # cloudinary.config(
        #     cloud_name="dre8gizbd",
        #     api_key="385655952173491",
        #     api_secret="LvhhB9GqjT-K1AxAdCA9N5ltgEM",
        #     secure=True
        # )

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Upload to Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(file, folder="profile_pictures")
            user.profile_picture = upload_result["secure_url"]
            user.save()
            return Response(
                {"message": "Profile picture updated successfully!", "profile_picture": user.profile_picture},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("Error during Cloudinary upload:", str(e))  # Log exact error
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListUsersView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Retrieve a filtered list of users based on the role of the authenticated user.",
        responses={
            200: OpenApiResponse(response=UserSerializer(many=True), description="Filtered list of users."),
            403: OpenApiResponse(description="Permission denied."),
        },
        parameters=[
            OpenApiParameter(
                name="Authorization",
                description="Bearer <JWT token>",
                required=True,
                type=str,
                location=OpenApiParameter.HEADER,
            )
        ],
        tags=["users"],
    )
    def get(self, request):
        user = request.user

        # Filtering logic based on role
        if user.role == 'guide':
            # List advisors and coordinator
            users = User.objects.filter(role__in=['advisor', 'coordinator', 'guide'])
        elif user.role == 'visitor':
            # List coordinator, secretary, director, and advisors
            users = User.objects.filter(role__in=['coordinator', 'secretary', 'director', 'advisor'])
        elif user.role in ['coordinator', 'advisor', 'secretary', 'director']:
            # List everyone
            users = User.objects.all()
        else:
            # For any other roles, deny access
            return Response({"error": "You do not have permission to view this list."}, status=status.HTTP_403_FORBIDDEN)

        # Serialize the filtered user list
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
