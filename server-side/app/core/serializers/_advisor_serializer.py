from rest_framework import serializers
from core.models._Advisor import Advisor

class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = "__all__"