from django.db import models
from django.utils import timezone

class Hospital(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.IntegerField(default=0)  # Add this field

    def __str__(self):
        return self.name

class MedicalSupply(models.Model):
    name = models.CharField(max_length=255)
    total_quantity = models.IntegerField()  # Renamed from 'quantity' to 'total_quantity'

    def __str__(self):
        return self.name

class DistributionRecord(models.Model):
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    supply = models.ForeignKey('MedicalSupply', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)  # Keeps track of how much is distributed
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        supply_name = self.supply.name if self.supply else "Unknown Supply"
        return f"{supply_name} - {self.hospital.name} ({self.quantity})"
