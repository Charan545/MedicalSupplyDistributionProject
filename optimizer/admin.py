from django.contrib import admin
from .models import Hospital, MedicalSupply, DistributionRecord

admin.site.register(Hospital)
admin.site.register(MedicalSupply)
admin.site.register(DistributionRecord)
