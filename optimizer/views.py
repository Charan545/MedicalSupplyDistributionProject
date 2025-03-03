from rest_framework import viewsets
from .models import Hospital, MedicalSupply, DistributionRecord
from .serializers import HospitalSerializer, MedicalSupplySerializer, DistributionRecordSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import optimize_distribution
from django.http import JsonResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def optimize_view(request):
    if request.method == "POST":
        # Sample Optimization Logic (Replace with your actual logic)
        result = {
            "status": "Success",
            "message": "Optimization completed",
            "optimized_allocation": {
                "Hospital A": {"masks": 100, "gloves": 200},
                "Hospital B": {"masks": 150, "gloves": 180}
            }
        }
        return JsonResponse(result)  # Return JSON response
    
    return render(request, 'optimize.html')


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class MedicalSupplyViewSet(viewsets.ModelViewSet):
    queryset = MedicalSupply.objects.all()
    serializer_class = MedicalSupplySerializer

class DistributionRecordViewSet(viewsets.ModelViewSet):
    queryset = DistributionRecord.objects.all()
    serializer_class = DistributionRecordSerializer
