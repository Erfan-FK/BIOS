from core.models._TourRequestBatch import TourRequestBatch
from core.serializers._tour_request_serializer import TourRequestSerializer
from core.serializers._visitor_serializer import VisitorUserSerializer
from core.serializers._tour_serializer import TourSerializer
from rest_framework import serializers

class TourRequestBatchSerializer(serializers.ModelSerializer):
    tour_requests = TourRequestSerializer(many=True, read_only=True)
    visitor = VisitorUserSerializer(read_only=True)
    tour = TourSerializer(read_only=True)

    class Meta:
        model = TourRequestBatch
        fields = "__all__"