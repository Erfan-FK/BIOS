from rest_framework import serializers
from core.models._TourReport import TourReport

class TourReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourReport 
        fields = "__all__"