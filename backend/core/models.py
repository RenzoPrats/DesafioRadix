from django.db import models
from django.utils import timezone

# Create your models here.
class SensorData(models.Model):
    equipment_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.DecimalField(max_digits=10, decimal_places=2)