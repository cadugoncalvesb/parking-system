from django.db import models

class PaymentType(models.Model):
    description = models.CharField(max_length=20)
