from django.db import models
from django.contrib.postgres.fields import ArrayField
from core.models._User import User  
from core.models._Review import Review

def default_availability():
    return [0 for _ in range(28)]

class Guide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guide_profile', null=True)
    rating = models.FloatField(default=0.0)
    availability = ArrayField(
        models.IntegerField(),
        size=28, 
        default=default_availability 
    )
    reviewCount = models.IntegerField(default=0)
    def __str__(self):
        return f"Guide {self.user.name} with rating {self.rating} and availability {self.availability}"
