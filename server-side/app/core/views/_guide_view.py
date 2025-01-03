from rest_framework.viewsets import ModelViewSet
from core.models._Guide import Guide
from core.serializers._guide_serializer import GuideSerializer
from core.serializers._tour_serializer import TourSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class GuideViewSet(ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

    @action(detail=True, methods=['get'])
    def tours(self, request, pk=None):
        guide = self.get_object()
        tours = guide.tours.all()
        serializer = TourSerializer(tours, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def available_slots(self, request, pk=None):
        guide = self.get_object()
        #get the availability of the guide
        available_slots = guide.availability
        return Response(available_slots)
    
    #method to get all the guides that are available at given time and day. Those paramterers are pas
    @action(detail=False, methods=['get'])
    def available_guides(self, request, *args, **kwargs):
        day = request.query_params.get('day')
        slot = request.query_params.get('slot')
        index = int(day) * 4 + int(slot)
        guides = Guide.objects.all()
        filtered_guides = [
        guide for guide in guides if len(guide.availability) > index and guide.availability[index] == 1
    ]
        serializer = self.get_serializer(filtered_guides, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='add-availability')
    def add_availability(self, request, pk=None):
        guide = self.get_object()
        day = int(request.data.get('day'))
        slot = int(request.data.get('slot'))
        index = day * 4 + slot

        if 0 <= index < 28:
            availability = guide.availability
            availability[index] = 1
            guide.availability = availability
            guide.save()
            return Response({"message": "Availability added", "availability": guide.availability}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid day or slot"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='remove-availability')
    def remove_availability(self, request, pk=None):
        guide = self.get_object()
        day = int(request.data.get('day'))
        slot = int(request.data.get('slot'))
        index = day * 4 + slot
        
        if 0 <= index < 28:
            availability = guide.availability
            availability[index] = 0
            guide.availability = availability
            guide.save()
            return Response({"message": "Availability removed", "availability": guide.availability}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid day or slot"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'], url_path='update-availability')
    def update_availability(self, request, pk=None):
        guide = self.get_object()
        source_day = int(request.data.get('source_day'))
        source_slot = int(request.data.get('source_slot'))
        target_day = int(request.data.get('target_day'))
        target_slot = int(request.data.get('target_slot'))

        source_index = source_day * 4 + source_slot
        target_index = target_day * 4 + target_slot

        if 0 <= source_index < 28 and 0 <= target_index < 28:
            availability = guide.availability

            # Remove from source
            availability[source_index] = 0

            # Add to target
            availability[target_index] = 1

            guide.availability = availability
            guide.save()
            return Response(
                {"message": "Availability updated", "availability": guide.availability},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"error": "Invalid source or target indices"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='guides-by-id-list')
    def get_guides_by_id_list(self, request):
        # Get the list of guide IDs from the query parameters
        guide_ids_param = request.query_params.get('guide_ids')
        
        if not guide_ids_param:
            return Response({"error": "No guide IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Convert the comma-separated string to a list of integers
            guide_ids = [int(guide_id) for guide_id in guide_ids_param.split(',')]
        except ValueError:
            return Response({"error": "Invalid guide IDs. IDs must be integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter guides by the provided IDs
        guides = Guide.objects.filter(id__in=guide_ids)

        # Construct the response data with rating and user name
        result = [
            {
                "id": guide.id,
                "rating": guide.rating,
                "name": guide.user.name  # Access the related user's name
            }
            for guide in guides
        ]

        return Response(result, status=status.HTTP_200_OK)
    
