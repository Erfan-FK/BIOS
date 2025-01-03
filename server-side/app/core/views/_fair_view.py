from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.models._Fair import Fair
from core.serializers._fair_serializer import FairInputSerializer, FairSerializer

class FairViewSet(ModelViewSet):
    queryset = Fair.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FairInputSerializer
        return FairSerializer

    @action(detail=False, methods=['get'], url_path='fair-requests')
    def get_fair_requests(self, request):
        fairs = Fair.objects.all()
        serializer = self.get_serializer(fairs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], url_path='approve')
    def approve_fair_request(self, request, pk=None):
        fair = self.get_object()
        fair.status = 'approved'
        fair.save()
        return Response({"status": "Fair approved"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], url_path='reject')
    def reject_fair_request(self, request, pk=None):
        fair = self.get_object()
        reason = request.data.get('reason', '')
        fair.status = 'rejected'
        fair.rejectionReason = reason
        fair.save()
        return Response({"status": "Fair rejected"}, status=status.HTTP_200_OK)