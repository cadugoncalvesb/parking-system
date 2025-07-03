from django.db import models
from entryRecord.models import EntryRecord
from paymentType.models import PaymentType
from django.utils.timezone import now
from datetime import datetime
import math

class ExitRecord(models.Model):
    exitDate = models.DateTimeField(default=now)
    finalValue = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    entryRecord = models.ForeignKey(EntryRecord, on_delete=models.CASCADE)
    paymentType = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Saída de {self.entry_record.plate} em {self.exit_date.strftime('%d/%m/%Y %H:%M')}"
    
