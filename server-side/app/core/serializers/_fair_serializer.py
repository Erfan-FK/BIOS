from rest_framework import serializers
from core.models._Fair import Fair
from core.serializers._visitor_serializer import VisitorUserSerializer

class FairInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fair
        fields = "__all__"

class FairSerializer(serializers.ModelSerializer):
    visitor = VisitorUserSerializer(read_only=True)
    class Meta:
        model = Fair
        fields = "__all__"