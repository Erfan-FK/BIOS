from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.models._Tour import Tour
from core.models._Guide import Guide
from core.models._Visitor import Visitor
from core.models._Advisor import Advisor
from core.serializers._tour_serializer import TourSerializer, CompletedTourSerializer
from core.serializers._review_serializer import ReviewSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.shortcuts import get_object_or_404

class TourViewSet(ModelViewSet):
    """ViewSet for managing tours."""
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    
    # Endpoint to get tours for a specific guide by guide ID
    @extend_schema(
        parameters=[
            OpenApiParameter(name='guide_id', location=OpenApiParameter.PATH, description='The ID of the guide', required=True, type=int)
        ]
    )
    @action(detail=False, methods=['get'], url_path='guide-tours/(?P<guide_id>[^/.]+)')
    def get_tours_by_guide(self, request, guide_id=None):
        try:
            guide = Guide.objects.get(pk=guide_id)
            tours = Tour.objects.filter(guides=guide)
            serializer = self.get_serializer(tours, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Guide.DoesNotExist:
            return Response({"error": "Guide not found."}, status=status.HTTP_404_NOT_FOUND)
        
    # Endpoint to get tours for a specific visitor by visitor ID
    @action(detail=False, methods=['get'], url_path='visitor-tours/(?P<visitor_id>[^/.]+)')
    def get_tours_by_visitor(self, request, visitor_id=None):
        try:
            visitor = Visitor.objects.get(pk=visitor_id)
            tours = Tour.objects.filter(visitor=visitor)
            serializer = self.get_serializer(tours, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Visitor.DoesNotExist:
            return Response({"error": "Visitor not found."}, status=status.HTTP_404_NOT_FOUND)

    # Endpoint to fetch tours for a specific date
    @action(detail=False, methods=['get'], url_path='tours-by-date')
    def get_tours_by_date(self, request):
        date = request.query_params.get('date')
        if date:
            tours = Tour.objects.filter(date=date)
            serializer = self.get_serializer(tours, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Date parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    # New Reject Tour Endpoint
    @action(detail=True, methods=['post'], url_path='reject')
    def reject_tour(self, request, pk=None):
        try:
            tour = Tour.objects.get(pk=pk)
        except Tour.DoesNotExist:
            return Response({"error": "Tour not found."}, status=status.HTTP_404_NOT_FOUND)

        guide_id = request.data.get('guide_id')
        if not guide_id:
            return Response({"error": "guide_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            guide = Guide.objects.get(pk=guide_id)
        except Guide.DoesNotExist:
            return Response({"error": "Guide not found."}, status=status.HTTP_404_NOT_FOUND)

        # Remove the guide from the tour
        tour.guides.remove(guide)

        # Check if there are no remaining guides
        if tour.guides.count() == 0:
            tour.status = 'UNASSIGNED'
        
        tour.save()

        serializer = self.get_serializer(tour)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='completed-tours-of-advisor')
    def get_completed_tours_of_advisor(self, request, pk=None):
        """
        Retrieves all completed tours for the advisor identified by pk
        that occur on their authorized days.
        """
        # Retrieve the advisor using the primary key from the URL
        advisor = get_object_or_404(Advisor, pk=pk)

        authorized_days = advisor.authorizedDay  # List of 7 integers
        if not any(authorized_days):
            return Response(
                {"message": "No authorized days set for this advisor.", "tours": []},
                status=status.HTTP_200_OK
            )
        
        # Map authorizedDay indices to Django's week_day (1=Sunday, 7=Saturday)
        week_day_mapping = {
            0: 2,  # Monday
            1: 3,  # Tuesday
            2: 4,  # Wednesday
            3: 5,  # Thursday
            4: 6,  # Friday
            5: 7,  # Saturday
            6: 1,  # Sunday
        }

        authorized_week_days = [
            week_day_mapping[i % 7]
            for i in range(len(authorized_days)) if authorized_days[i]
    ]   

        if not authorized_week_days:
            return Response(
                {"message": "No authorized days set for this advisor.", "tours": []},
                status=status.HTTP_200_OK
            )

        # Filter Tours based on status, advisor, and authorized days
        tours = Tour.objects.filter(
            status='COMPLETED',
            date__week_day__in=authorized_week_days
        )

        if not tours.exists():
            return Response(
                {"message": "No completed tours found on authorized days.", "tours": []},
                status=status.HTTP_200_OK
            )

        serializer = CompletedTourSerializer(tours, many=True)
        return Response({"tours": serializer.data}, status=status.HTTP_200_OK)
        
        
    # Return the review of a tour with given ID

    @action(detail=True, methods=['get'], url_path='get-review')
    def get_review(self, request, pk=None):
        try:
            tour = Tour.objects.get(pk=pk)
            review = tour.review
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tour.DoesNotExist:
            return Response({"error": "Tour not found."}, status=status.HTTP_404_NOT_FOUND)

        


    # Endpoint to post a review for a tour
    @action(detail=True, methods=['post'], url_path='post-review')
    def post_review(self, request, pk=None):
        try:
            tour = Tour.objects.get(pk=pk)
        except Tour.DoesNotExist:
            return Response({"error": "Tour not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save()
            tour.review = review
            tour.save()

            # Update the review count and rating for each guide associated with the tour
            for guide in tour.guides.all():
                guide.reviewCount += 1
                guide.rating = (guide.rating * (guide.reviewCount - 1) + review.reviewRating) / guide.reviewCount
                guide.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Endpoint to get tours for a specific visitor by visitor ID
    @extend_schema(
        parameters=[
            OpenApiParameter(name='visitor_id', location=OpenApiParameter.PATH, description='The ID of the visitor', required=True, type=int)
        ]
    )
    @action(detail=False, methods=['get'], url_path='visitor-tours/(?P<visitor_id>[^/.]+)')
    def get_tours_by_visitor(self, request, visitor_id=None):
        try:
            visitor = Visitor.objects.get(pk=visitor_id)
            tours = Tour.objects.filter(visitor=visitor)
            serializer = self.get_serializer(tours, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Visitor.DoesNotExist:
            return Response({"error": "Visitor not found."}, status=status.HTTP_404_NOT_FOUND)
    # Endpoint to get tours for a specific advisor by advisor ID
    @extend_schema(
        parameters=[
            OpenApiParameter(name='advisor_id', location=OpenApiParameter.PATH, description='The ID of the advisor', required=True, type=int)
        ]
    )
    @action(detail=False, methods=['get'], url_path='advisor-tours/(?P<advisor_id>[^/.]+)')
    def get_tours_by_advisor(self, request, advisor_id=None):
        try:
            advisor = Advisor.objects.get(pk=advisor_id)

            authorized_days = advisor.authorizedDay  # List of 7 integers
            if not any(authorized_days):
                return Response(
                    {"error": "No authorized days set for this advisor."},
                    status=status.HTTP_200_OK
                )

            # Map authorizedDay indices to Django's week_day (1=Sunday, 7=Saturday)
            week_day_mapping = {
                0: 2,  # Monday
                1: 3,  # Tuesday
                2: 4,  # Wednesday
                3: 5,  # Thursday
                4: 6,  # Friday
                5: 7,  # Saturday
                6: 1,  # Sunday
            }

            authorized_week_days = [
                week_day_mapping[i]
                for i in authorized_days
            ]

            if not authorized_week_days:
                return Response(
                    {"error": "No authorized days set for this advisor."},
                    status=status.HTTP_200_OK
                )

            # Filter Tours based on status, advisor, and authorized days
            tours = Tour.objects.filter(
                date__week_day__in=authorized_week_days
            )

            if not tours.exists():
                return Response(
                    {"message": "No tours found on authorized days."},
                    status=status.HTTP_200_OK
                )
            serializer = CompletedTourSerializer(tours, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Advisor.DoesNotExist:
            return Response({"error": "Advisor not found."}, status=status.HTTP_404_NOT_FOUND)