from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HospitalViewSet, MedicalSupplyViewSet, DistributionRecordViewSet, 
    home, optimize, result_view, get_optimization_data
)

router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet)
router.register(r'supplies', MedicalSupplyViewSet)
router.register(r'distributions', DistributionRecordViewSet)

urlpatterns = [
    path('', home, name='home'), 
    path('api/', include(router.urls)),
    path('optimize/', optimize, name='optimize'),
    path('result/', result_view, name='result'),
    path('api/optimization-data/', get_optimization_data, name='optimization_data'),
]
