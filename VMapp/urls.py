from django.urls import path
from .views import VendorListCreate,VendorModify,PurchaseorderListCreate,PurchaseorderModify,VendorPerformance,Acknowledgement
urlpatterns = [
    path('vendors/', VendorListCreate.as_view(), name='vendorlistcreate'),
    path('vendors/<str:pk>/', VendorModify.as_view(), name='vendorModify'),
    path('purchaseorders/', PurchaseorderListCreate.as_view(), name='purchaseorderlist'),
    path('purchaseorders/<str:pk>/', PurchaseorderModify.as_view(), name='purchaseorderModify'),
    path('vendors/<str:pk>/performance/', VendorPerformance.as_view(), name='vendorperformance'),
    path('purchaseorders/<str:pk>/acknowledge/', Acknowledgement.as_view(), name='acknowledgement'),
]