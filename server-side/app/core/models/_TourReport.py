from django.db import models
from core.models._Tour import Tour
from core.models._Guide import Guide

class TourReport (models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reports')
    report = models.TextField()
    finishedAtHour = models.IntegerField()
    finishedAtMinute = models.IntegerField()
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='reports')    