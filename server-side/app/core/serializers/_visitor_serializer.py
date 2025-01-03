from rest_framework import serializers

from core.models._Visitor import Visitor
from core.serializers._user_serializer import UserSerializer


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"

class VisitorUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Visitor
        fields = "__all__"