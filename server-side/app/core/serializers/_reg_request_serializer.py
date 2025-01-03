from rest_framework import serializers
from core.models._RegRequest import RegRequest

class RegRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegRequest
        fields = "__all__"
    