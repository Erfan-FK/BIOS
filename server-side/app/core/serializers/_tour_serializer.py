from rest_framework import serializers
from core.models._Tour import Tour
from core.models._Review import Review
from core.models._Visitor import Visitor
from core.serializers._visitor_serializer import VisitorSerializer, VisitorUserSerializer
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

class TourSerializer(serializers.ModelSerializer):
    visitor = VisitorSerializer(read_only=True)  # Only read, so returns nested object in GET
    visitor_id = serializers.IntegerField(write_only=True, required=False)  # Used for POST/PUT/PATCH
    review = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(),
        allow_null=True,
        required=False,
    )
    time_slot_id = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = "__all__"
        extra_fields = ['time_slot_id']

    @extend_schema_field(OpenApiTypes.STR)
    def get_time_slot_id(self, obj):
        time_slot_dict = dict(Tour.TIME_SLOTS)
        return time_slot_dict.get(obj.slot, "")

    def create(self, validated_data):
        visitor_id = validated_data.pop('visitor_id', None)
        if visitor_id:
            # Fetch the visitor instance
            try:
                visitor_instance = Visitor.objects.get(pk=visitor_id)
            except Visitor.DoesNotExist:
                raise serializers.ValidationError({"visitor_id": "Invalid visitor ID."})
            validated_data['visitor'] = visitor_instance

        return super().create(validated_data)

    def update(self, instance, validated_data):
        visitor_id = validated_data.pop('visitor_id', None)
        if visitor_id:
            try:
                visitor_instance = Visitor.objects.get(pk=visitor_id)
            except Visitor.DoesNotExist:
                raise serializers.ValidationError({"visitor_id": "Invalid visitor ID."})
            validated_data['visitor'] = visitor_instance

        return super().update(instance, validated_data)

class CompletedToursInputSerializer (serializers.Serializer):
    advisor_id = serializers.IntegerField()

class CompletedTourSerializer(TourSerializer):
    visitor = VisitorUserSerializer(read_only=True)