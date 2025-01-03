from django.db import models
from core.constants import REQUEST_STATUS, REG_USER_TYPE_CHOICES


class RegRequest(models.Model):
    name = models.CharField(max_length=255)  
    email = models.EmailField(max_length=255, unique=True)  
    phone_no = models.CharField(max_length=20)  
    user_type = models.CharField(max_length=50, choices=REG_USER_TYPE_CHOICES)  
    high_school_name = models.CharField(max_length=255, blank=True, null=True)  
    city = models.CharField(max_length=255, blank=True, null=True)  
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=REQUEST_STATUS, default='pending')

