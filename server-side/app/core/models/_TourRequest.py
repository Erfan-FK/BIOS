from django.db import models
from core.constants import REQUEST_STATUS, TIME_SLOTS
from core.models._Visitor import Visitor
from core.models._TourRequestBatch import TourRequestBatch

class TourRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    batch = models.ForeignKey(TourRequestBatch, on_delete=models.CASCADE, related_name='tour_requests')
    date = models.DateField(default=None)
    time_slot = models.CharField(max_length=11, choices=TIME_SLOTS)