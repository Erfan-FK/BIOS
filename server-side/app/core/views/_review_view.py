from rest_framework.viewsets import ModelViewSet
from core.models._Review import Review 
from core.serializers._review_serializer import ReviewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models._Guide import Guide
from core.models._Tour import Tour

class ReviewViewSet(ModelViewSet):
    """ViewSet for managing reviews."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class GuideReviewsView(APIView):
    def get(self, request, guide_id):
        try:
            # Retrieve the guide object
            guide = Guide.objects.get(pk=guide_id)
            
            # Get all tours associated with this guide
            tours = Tour.objects.filter(guides=guide)
            
            # Get all reviews linked to these tours
            reviews = Review.objects.filter(tours__in=tours).distinct()
            
            # Serialize the reviews
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Guide.DoesNotExist:
            return Response({"error": "Guide not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)