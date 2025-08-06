from django.db import models

class VehicleType(models.Model): 
    category = models.CharField(max_length=20, verbose_name="Categoria:")
    valuePerVehicle = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Valor por veículo:")

    def __str__(self):
        return self.category
    
     # para que a placa seja salva em maiúsculo
    def save(self, *args, **kwargs):
        self.category = self.category.upper()
        super().save(*args, **kwargs)