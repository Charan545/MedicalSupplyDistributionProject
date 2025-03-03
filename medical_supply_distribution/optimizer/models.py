from django.db import models
from django.utils import timezone

class Hospital(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, null=True, blank=True)  # Allows blank values

    def __str__(self):
        return self.name

class MedicalSupply(models.Model):
    name = models.CharField(max_length=100, unique=True)
    total_quantity = models.IntegerField(default=0)  # Ensuring default value is an integer

    def __str__(self):
        return self.name

class DistributionRecord(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    supply = models.ForeignKey(MedicalSupply, on_delete=models.CASCADE)  # Corrected ForeignKey
    quantity = models.IntegerField(default=0)  # Ensuring a valid integer default
    timestamp = models.DateTimeField(default=timezone.now, editable=False)  # Correct DateTime default

    def __str__(self):
        return f"{self.supply.name} - {self.hospital.name} ({self.quantity})"
