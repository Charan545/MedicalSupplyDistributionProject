from rest_framework import serializers
from .models import Hospital, MedicalSupply, DistributionRecord

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class MedicalSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalSupply
        fields = '__all__'

class DistributionRecordSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)
    supply = MedicalSupplySerializer(read_only=True)

    class Meta:
        model = DistributionRecord
        fields = '__all__'
