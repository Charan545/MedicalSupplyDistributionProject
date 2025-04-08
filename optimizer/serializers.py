from rest_framework import serializers
from .models import Hospital, MedicalSupply, DistributionRecord

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'location']

class MedicalSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalSupply
        fields = ['id', 'name', 'total_quantity']  # Ensure 'total_quantity' is used

class DistributionRecordSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    supply_name = serializers.CharField(source='supply.name', read_only=True)

    class Meta:
        model = DistributionRecord
        fields = ['id', 'hospital', 'hospital_name', 'supply', 'supply_name', 'quantity', 'timestamp']
