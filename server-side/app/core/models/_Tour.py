from django.db import models
from core.constants import TIME_SLOTS
from core.models._Visitor import Visitor
from core.models._Guide import Guide
from core.models._Review import Review

class Tour(models.Model):
    TOUR_STATUS = (
        ('UNASSIGNED', 'Unassigned'),
        ('ASSIGNED', 'Assigned'),
        ('COMPLETED', 'Completed'),
    )

    TIME_SLOTS = TIME_SLOTS
    date = models.DateField()
    slot = models.CharField(max_length=10, choices=TIME_SLOTS)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='tours')
    guides = models.ManyToManyField(Guide, related_name='tours', blank=True)
    review = models.OneToOneField(Review, related_name='tours', blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=TOUR_STATUS, default='UNASSIGNED')

def save(self, *args, **kwargs):
    # First save: assign PK
    initial_create = self.pk is None
    super(Tour, self).save(*args, **kwargs)

    # If this is not the initial create, or if we want to re-check after creation
    if not initial_create:
        self._update_status()

def _update_status(self):
    # Logic to update status based on self.guides
    if self.guides.exists():
        self.status = 'ASSIGNED'
    else:
        from datetime import date
        self.status = 'COMPLETED' if self.date < date.today() else 'UNASSIGNED'
    super(Tour, self).save(update_fields=['status'])