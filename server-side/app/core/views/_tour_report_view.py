from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.models._TourReport import TourReport
from core.serializers._tour_report_serializer import TourReportSerializer

class TourReportViewSet(ModelViewSet):
    queryset = TourReport.objects.all()
    serializer_class = TourReportSerializer

    @action(detail=False, methods=['get'], url_path='by-tour/(?P<tour_id>[^/.]+)')
    def get_report_by_tour_id(self, request, tour_id=None):
        tour_reports = TourReport.objects.filter(tour_id=tour_id)
        if tour_reports.exists():
            serializer = TourReportSerializer(tour_reports, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)