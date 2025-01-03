from core.models._TourRequest import TourRequest
from rest_framework import serializers

class TourRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourRequest
        fields = "__all__"

class TourRequestInputSerializer(serializers.Serializer):
    dates = serializers.ListField(
        child=serializers.DateField(),
        required=True
    )
    time_slots = serializers.ListField(
        child=serializers.ChoiceField(choices=TourRequest._meta.get_field('time_slot').choices),
        required=True
    )
    visitor_id = serializers.IntegerField(required=True)
    additional_notes = serializers.CharField(required=False, allow_blank=True)
    number_of_visitors = serializers.IntegerField(required=True)