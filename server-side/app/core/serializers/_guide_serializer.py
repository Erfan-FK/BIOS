from rest_framework import serializers
from core.models._Guide import Guide
from core.serializers._user_serializer import UserSerializer

class GuideSerializer(serializers.ModelSerializer):
    formatted_availability = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    class Meta:
        model = Guide
        fields = "__all__"

        

    def get_formatted_availability(self, obj):
        daysOfWeek = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]
        timeSlots = ["9:00 am - 11:00 am", "11:00 am - 1:00 pm", "1:30 pm - 4:00 pm", "4:00 pm - 5:30 pm"]
        
        result = []
        for dayIndex in range(7):
            for slotIndex in range(4):
                index = dayIndex * 4 + slotIndex
                if obj.availability[index] == 1:
                    result.append({
                        "day": daysOfWeek[dayIndex],
                        "slot": timeSlots[slotIndex]
                    })
        return result