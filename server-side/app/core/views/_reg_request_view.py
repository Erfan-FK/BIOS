from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status as drf_status
from rest_framework.viewsets import ModelViewSet
from core.models._RegRequest import RegRequest
from core.serializers._reg_request_serializer import RegRequestSerializer
from core.models._User import User
from django.utils.crypto import get_random_string
from core.utils import send_email, send_rejection_email 


class RegRequestViewSet(ModelViewSet):
    queryset = RegRequest.objects.all()
    serializer_class = RegRequestSerializer

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_request(self, request, pk=None):
        try:
            # Get the registration request
            reg_request = self.get_object()

            # Debug log
            print(f"Approving Registration Request ID: {pk}")

            # Generate a random password (plain text)
            random_password = get_random_string(length=8)
            
            # Create the user (plain-text password is passed here)
            user = User.objects.create_user(
                email=reg_request.email,
                password=random_password,  # Pass the plain-text password
                name=reg_request.name,
                role="visitor",
            )
            print(f"User created: {user.id}, Email: {user.email}")

            # Update the visitor profile created by UserManager
            visitor = user.visitor_profile  # Access the Visitor profile linked to the user
            visitor.type = (
                "high-school" if reg_request.user_type == "high_school_counsellor" else "individual"
            )
            visitor.highSchoolName = reg_request.high_school_name
            visitor.contactNumber = reg_request.phone_no
            visitor.city = reg_request.city
            visitor.save()
            print(f"Visitor profile updated for User ID: {user.id}")

            # Send the email with the plain-text password
            send_email(
                to_email=reg_request.email,
                receiver=reg_request.name,
                password=random_password,  # Send plain-text password to the user
            )
            
            # Delete the registration request
            reg_request.delete()
            
            return Response({"message": "Request approved successfully."}, status=drf_status.HTTP_200_OK)
        except Exception as e:
            # Log and return the error
            print(f"Error during approval: {str(e)}")
            return Response({"error": str(e)}, status=drf_status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject_request(self, request, pk=None):
        try:
            reg_request = self.get_object()
            rejection_reason = request.data.get('reason', '').strip()

            if not rejection_reason:
                return Response(
                    {"error": "Rejection reason is required."},
                    status=drf_status.HTTP_400_BAD_REQUEST
                )

            # Extract user details from the registration request
            user_email = reg_request.email
            user_name = reg_request.name

            # Send the rejection email
            send_rejection_email(
                to_email=user_email,
                receiver=user_name,
                rejection_reason=rejection_reason
            )

            # Delete the registration request
            reg_request.delete()

            return Response(
                {"message": "Request rejected successfully.", "reason": rejection_reason},
                status=drf_status.HTTP_200_OK
            )
        except Exception as e:
            # Log and return the error
            print(f"Error during rejection: {str(e)}")
            return Response({"error": str(e)}, status=drf_status.HTTP_400_BAD_REQUEST)
