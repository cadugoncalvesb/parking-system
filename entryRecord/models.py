from django.db import models
from vehicleType.models import VehicleType
from django.utils.timezone import now

class EntryRecord(models.Model):
    plate = models.CharField(max_length=7)
    entryDate = models.DateTimeField(default=now)
    vehicleType = models.ForeignKey(VehicleType, on_delete=models.CASCADE)

    # para que a placa seja salva em maiúsculo
    def save(self, *args, **kwargs):
        self.plate = self.plate.upper()
        super().save(*args, **kwargs)

