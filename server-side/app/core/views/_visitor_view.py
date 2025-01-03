from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.models._Visitor import Visitor
from core.models._TourRequestBatch import TourRequestBatch
from core.serializers._visitor_serializer import VisitorSerializer
from core.serializers._tour_request_batch_serializer import TourRequestBatchSerializer

class VisitorViewSet(ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    @action(detail=True, methods=['get'], url_path='tour-request-batches')
    def get_tour_request_batches(self, request, pk=None):
        try:
            visitor = self.get_object()
            tour_request_batches = TourRequestBatch.objects.filter(visitor=visitor)
            serializer = TourRequestBatchSerializer(tour_request_batches, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Visitor.DoesNotExist:
            return Response({"error": "Visitor not found."}, status=status.HTTP_404_NOT_FOUND)