from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HospitalViewSet, MedicalSupplyViewSet, DistributionRecordViewSet
from .views import home
from .views import home, optimize_view  # Import the correct views


router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet)
router.register(r'supplies', MedicalSupplyViewSet)
router.register(r'distributions', DistributionRecordViewSet)

urlpatterns = [
    path('', home, name='home'), 
    path('api/', include(router.urls)),
    path('optimize/', optimize_view, name='optimize'),  # ✅ Named 'optimize'

]
