from rest_framework import viewsets
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Hospital, MedicalSupply, DistributionRecord
from .serializers import HospitalSerializer, MedicalSupplySerializer, DistributionRecordSerializer
from .optimizer_logic import optimize_distribution  # Ensure this file exists
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
# Home Page
def home(request):
    return render(request, 'home.html')

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import json

@csrf_exempt
def optimize(request):
    if request.method == "GET":
        return render(request, "optimize.html")

    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            supply = np.array(data['supply'])
            demand = np.array(data['demand'])
            cost_matrix = np.array(data['cost_matrix'])

            if cost_matrix.shape != (len(supply), len(demand)):
                return JsonResponse({
                    'success': False,
                    'error': "Cost matrix dimensions do not match supply and demand"
                }, status=400)

            optimized_distribution = optimize_distribution(supply, demand, cost_matrix)

            return JsonResponse({
                'success': True,
                'message': 'Optimization successful',
                'distribution': optimized_distribution.tolist()
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


from scipy.optimize import linprog

def optimize_distribution(supply, demand, cost_matrix):
    num_centers = len(supply)
    num_hospitals = len(demand)
    
    c = cost_matrix.flatten()

    # Inequality matrix for supply constraints
    A_eq = []
    b_eq = []

    # Supply constraints
    for i in range(num_centers):
        constraint = [0] * (num_centers * num_hospitals)
        for j in range(num_hospitals):
            constraint[i * num_hospitals + j] = 1
        A_eq.append(constraint)
        b_eq.append(supply[i])

    # Demand constraints
    for j in range(num_hospitals):
        constraint = [0] * (num_centers * num_hospitals)
        for i in range(num_centers):
            constraint[i * num_hospitals + j] = 1
        A_eq.append(constraint)
        b_eq.append(demand[j])

    # Bounds: each variable >= 0
    bounds = [(0, None) for _ in range(num_centers * num_hospitals)]

    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    if res.success:
        result = np.array(res.x).reshape((num_centers, num_hospitals))
        return np.round(result).astype(int)
    else:
        raise ValueError("Optimization failed")

def get_optimization_data(request):
    try:
        hospitals = Hospital.objects.all()
        supplies = MedicalSupply.objects.all()

        hospital_data = {hospital.name: hospital.capacity for hospital in hospitals}
        supply_data = {supply.name: supply.total_quantity for supply in supplies}  # Fix reference

        return JsonResponse({
            'hospitals': hospital_data,
            'supplies': supply_data
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Results Page
def result_view(request):
    supply = [20, 30, 50]  # Supply from sources
    demand = [30, 40, 30]  # Demand at hospitals
    cost_matrix = [
        [8, 6, 10],
        [9, 7, 4],
        [3, 4, 2]
    ]

    # Run Optimization Logic
    optimized_cost = optimize_distribution(supply, demand, cost_matrix)

    return render(request, 'result.html', {'cost_data': optimized_cost})

# API ViewSets
class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class MedicalSupplyViewSet(viewsets.ModelViewSet):
    queryset = MedicalSupply.objects.all()
    serializer_class = MedicalSupplySerializer

class DistributionRecordViewSet(viewsets.ModelViewSet):
    queryset = DistributionRecord.objects.all()
    serializer_class = DistributionRecordSerializer
