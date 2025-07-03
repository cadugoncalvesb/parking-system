from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    phone = models.CharField(max_length=11)
    password = models.CharField(max_length=128)
    isAdmin = models.BooleanField(default=False)
