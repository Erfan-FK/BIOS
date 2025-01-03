from rest_framework import serializers
from core.models._Review import Review
from core.models._Tour import Tour
from core.serializers._visitor_serializer import VisitorUserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.SerializerMethodField()
    tour_id = serializers.IntegerField(write_only=True)  # Accept tour ID on creation

    class Meta:
        model = Review
        fields = ['id', 'review', 'reviewRating', 'timestamp', 'reviewer', 'tour_id']

    def get_reviewer(self, obj):
        try:
            tour = Tour.objects.get(review=obj)
            if tour.visitor:
                return VisitorUserSerializer(tour.visitor).data
        except Tour.DoesNotExist:
            return None
        return None

    def create(self, validated_data):
        tour_id = validated_data.pop('tour_id')
        try:
            tour = Tour.objects.get(pk=tour_id)
        except Tour.DoesNotExist:
            raise serializers.ValidationError({'tour_id': 'Invalid tour ID'})

        # Ensure the reviewer matches the visitor of the tour
        if not tour.visitor:
            raise serializers.ValidationError({'tour_id': 'Tour has no associated visitor'})

        # Create the review
        review = Review.objects.create(**validated_data)

        # Link the review to the tour
        tour.review = review
        tour.save()
        return review