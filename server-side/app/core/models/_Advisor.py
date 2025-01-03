from django.db import models
from django.contrib.postgres.fields import ArrayField
from core.models._User import User

def default_authorized_day():
    return []

class Advisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='advisor_profile', null=True) 
    authorizedDay = ArrayField(
        models.IntegerField(),
        size=7, 
        default=default_authorized_day
    )
    isCoordinator = models.BooleanField(default=False)