from rest_framework.viewsets import ModelViewSet
from core.models._TourRequest import TourRequest
from core.serializers._tour_request_serializer import TourRequestSerializer


class TourRequestViewSet(ModelViewSet):
    """ViewSet for managing tours."""
    queryset = TourRequest.objects.all()
    serializer_class = TourRequestSerializer