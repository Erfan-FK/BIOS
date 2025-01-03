from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.models._Advisor import Advisor
from core.models._Guide import Guide
from core.models._Tour import Tour
from core.models._TourReport import TourReport
from core.models._TourRequest import TourRequest
from core.models._Visitor import Visitor
from core.serializers._advisor_serializer import AdvisorSerializer
from django.core.mail import EmailMessage
from openpyxl import Workbook
from datetime import datetime, timedelta
import io

class AdvisorViewSet(ModelViewSet):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    
    @action(detail=False, methods=['get'], url_path='completed-tours-count')
    def get_completed_tours_count(self, request):
        completed_tours_count = Tour.objects.filter(status='COMPLETED').count()
        return Response({"completed_tours_count": completed_tours_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='tour-requests-count')
    def get_tour_requests_count(self, request):
        tour_requests_count = TourRequest.objects.count()
        return Response({"tour_requests_count": tour_requests_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='rejected-tours-count')
    def get_rejected_tours_count(self, request):
        rejected_tours_count = Tour.objects.filter(status='REJECTED').count()
        return Response({"rejected_tours_count": rejected_tours_count}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='total-visitors-count')
    def get_total_visitors_count(self, request):
        total_visitors_count = Visitor.objects.count()
        return Response({"total_visitors_count": total_visitors_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='total-guides-count')
    def get_total_guides_count(self, request):
        total_guides_count = Guide.objects.count()
        return Response({"total_guides_count": total_guides_count}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='guides-ratings')
    def get_guides_ratings(self, request):
        guides = Guide.objects.all()
        guides_ratings = [{"name": guide.user.name, "rating": guide.rating} for guide in guides]
        return Response({"guides_ratings": guides_ratings}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='send-guide-report')
    def send_guide_report(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create an Excel workbook and sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Guide Working Hours"
        ws.append(["Guide Name", "Visitor Name", "Visitor High School", "Tour Starting", "Tour End", "Total Hour"])

        one_month_ago = datetime.now() - timedelta(days=30)
        guides = Guide.objects.all()

        slot_to_hour = {
            '09.00 AM': '9.00',
            '11.00 AM': '11.00',
            '13.30 PM': '13.30',
            '16.00 PM': '16.00',
        }

        for guide in guides:
            for tour in guide.tours.filter(date__gte=one_month_ago, status='COMPLETED'):
                try:
                    report = TourReport.objects.get(tour=tour, guide=guide)
                    start_hour = slot_to_hour[tour.slot]
                    end_hour = report.finishedAtHour + report.finishedAtMinute / 60
                    total_hour = round(end_hour - float(start_hour), 2)
                    ws.append([
                        guide.user.name,
                        tour.visitor.user.name,
                        tour.visitor.highSchoolName,
                        start_hour,
                        f"{report.finishedAtHour}.{report.finishedAtMinute:02d}",
                        total_hour
                    ])
                except TourReport.DoesNotExist:
                    continue

        # Save the workbook to a bytes buffer
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        # Send the email with the Excel attachment
        email_message = EmailMessage(
            subject="Guide Working Hours Report",
            body="Please find the attached report for guide working hours.",
            to=[email]
        )
        email_message.attach("guide_working_hours.xlsx", buffer.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        email_message.send()

        return Response({"message": "Report sent successfully."}, status=status.HTTP_200_OK)