from django.db import models
from core.models._Visitor import Visitor

class Fair(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]

    explanation = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    visitor = models.OneToOneField(Visitor, on_delete=models.CASCADE, related_name='fair')
    date = models.DateField(default=None)

    def __str__(self):
        return f"Fair {self.name} at {self.schoolName}"