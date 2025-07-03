from django.db import models

class Parking(models.Model):
    totalVacancies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.totalVacancies} vagas"
