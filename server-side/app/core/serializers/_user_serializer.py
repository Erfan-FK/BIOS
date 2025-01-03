from rest_framework import serializers
from core.models._User import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
     
    class Meta:
        model = User
        fields = "__all__"