from django.db import models
from core.constants import REQUEST_STATUS, TIME_SLOTS
from core.models._Visitor import Visitor
from core.models._Tour import Tour

class TourRequestBatch(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='tour_request_batch')
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')
    additional_notes = models.TextField(blank=True, null=True)
    number_of_visitors = models.IntegerField(default=1)
    rejection_reason = models.TextField(blank=True, null=True)
    tour = models.OneToOneField(Tour, on_delete=models.SET_NULL, related_name='tour_request_batch', blank=True, null=True)