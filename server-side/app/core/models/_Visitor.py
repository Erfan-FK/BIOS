from django.db import models
from core.models._User import User
from core.constants import VISITOR_TYPE_CHOICES


class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='visitor_profile', null=True)
    type = models.CharField(max_length=20, choices=VISITOR_TYPE_CHOICES)
    highSchoolName = models.TextField(blank=True, null=True)
    contactNumber = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.type})"
