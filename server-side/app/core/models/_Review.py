from django.db import models

class Review(models.Model):
    review = models.TextField()
    reviewRating = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)