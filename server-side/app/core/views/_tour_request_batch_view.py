from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.models._TourRequestBatch import TourRequestBatch
from core.models._TourRequest import TourRequest
from core.models._Visitor import Visitor
from core.serializers._tour_request_batch_serializer import TourRequestBatchSerializer
from core.serializers._tour_request_serializer import TourRequestInputSerializer  # New input serializer
from core.serializers._tour_serializer import TourSerializer
from django.shortcuts import get_object_or_404


class TourRequestBatchViewSet(ModelViewSet):
    """ViewSet for managing tour request batches."""
    queryset = TourRequestBatch.objects.all()
    serializer_class = TourRequestBatchSerializer

    @action(detail=False, methods=['post'], url_path='create-with-requests')
    def create_with_requests(self, request):
        """Create a TourRequestBatch along with associated TourRequests."""
        input_serializer = TourRequestInputSerializer(data=request.data)

        if input_serializer.is_valid():
            data = input_serializer.validated_data
            visitor_id = data['visitor_id']
            dates = data['dates']
            time_slots = data['time_slots']
            additional_notes = data.get('additional_notes', "")
            number_of_visitors = data['number_of_visitors']

            # Get the visitor instance
            try:
                visitor = Visitor.objects.get(id=visitor_id)
            except Visitor.DoesNotExist:
                return Response({"error": "Visitor not found."}, status=status.HTTP_404_NOT_FOUND)

            # Create the TourRequestBatch
            batch = TourRequestBatch.objects.create(
                visitor=visitor,
                status='pending',
                additional_notes=additional_notes,
                number_of_visitors=number_of_visitors
            )

            # Create TourRequest entries for each date and time slot
            tour_requests = []
            for date,time_slot in zip(dates,time_slots):
                tour_requests.append(TourRequest(batch=batch, date=date, time_slot=time_slot))

            # Bulk create tour requests
            TourRequest.objects.bulk_create(tour_requests)

            # Serialize and return the created batch
            batch_serializer = self.get_serializer(batch)
            return Response(batch_serializer.data, status=status.HTTP_201_CREATED)

        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='schedule')
    def schedule(self, request, pk=None):
        """Schedule a TourRequestBatch."""
        input_serializer = TourSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        batch = self.get_object()

        # Check if there is an existing scheduled tour and delete it
        if batch.tour:
            # Only delete the tour without affecting the TourRequestBatch
            batch.tour.delete(keep_parents=True)

        # Schedule the new tour
        tour = input_serializer.save()
        batch.status = 'scheduled'
        batch.tour = tour
        batch.save()
        
        return Response({"message": "Batch scheduled successfully."}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='by-tour/(?P<tour_id>[^/.]+)')
    def get_request_batch_of_tour(self, request, tour_id=None):
        """Retrieve the TourRequestBatch associated with a specific tour_id."""
        tour_request_batch = get_object_or_404(TourRequestBatch, tour_id=tour_id)
        serializer = self.get_serializer(tour_request_batch)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='approved')
    def get_tour_approved_request_batches(self, request):
        """Retrieve all approved TourRequestBatch instances."""
        approved_batches = TourRequestBatch.objects.filter(status='approved')
        serializer = self.get_serializer(approved_batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='pending')
    def get_tour_pending_request_batches(self, request):
        """Retrieve all pending TourRequestBatch instances."""
        pending_batches = TourRequestBatch.objects.filter(status='pending')
        serializer = self.get_serializer(pending_batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)