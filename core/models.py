from django.db import models
from django.core.cache import cache


# Create your models here.
class VehicleLocation(models.Model):
    device_id = models.IntegerField()
    long = models.DecimalField(max_digits=25, decimal_places=20)
    lat = models.DecimalField(max_digits=25, decimal_places=20)
    ts = models.DateTimeField()
    sts = models.DateTimeField()
    speed = models.IntegerField()

    def __str__(self):
        return f"{self.device_id}"
