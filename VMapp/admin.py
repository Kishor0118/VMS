from django.contrib import admin
from .models import Vendor,Purchaseorder,Historicalperformance

admin.site.register(Vendor)
admin.site.register(Purchaseorder)
admin.site.register(Historicalperformance)