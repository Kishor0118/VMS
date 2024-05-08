from .models import Vendor,Purchaseorder
from .serializers import VendorSerializer,PurchaseorderSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,status
from django.db.models import Count



class VendorListCreate(generics.ListCreateAPIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes  = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer    
    
class VendorModify(generics.RetrieveUpdateDestroyAPIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes  = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseorderListCreate(generics.ListCreateAPIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes  = [IsAuthenticated]
    queryset = Purchaseorder.objects.annotate(total_orders=Count('po_number'))  # Provide an alias for Count aggregation
    serializer_class = PurchaseorderSerializer
    

class PurchaseorderModify(generics.RetrieveUpdateDestroyAPIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes  = [IsAuthenticated]
    queryset = Purchaseorder.objects.all()
    serializer_class  = PurchaseorderSerializer
    
class VendorPerformance(generics.RetrieveAPIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes  = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class  = VendorSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'on_time_delivery_rate': serializer.data['on_time_delivery_rate'],
                 'quality_rating_avg': serializer.data['quality_rating_avg'],
                 'average_response_time': serializer.data['average_response_time'],
                 'fulfillment_rate': serializer.data['fulfillment_rate']})


class Acknowledgement(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Purchaseorder.objects.all()
    serializer_class = PurchaseorderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        acknowledgment_date = instance.acknowledgment_date

        if acknowledgment_date:
            vendor = instance.vendor
            responsetimes = Purchaseorder.objects.filter(
                vendor=vendor, acknowledgment_date__isnull=False
            ).values_list('acknowledgment_date', 'issue_date')

            total_seconds = sum(
                abs((ack_date - issue_date).total_seconds())
                for ack_date, issue_date in responsetimes
            )

            average_response_time = total_seconds / len(responsetimes) if responsetimes else 0

            vendor.average_response_time = average_response_time
            vendor.save()

            return Response({'acknowledgment_date': acknowledgment_date}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid or missing acknowledgment date'}, status=status.HTTP_400_BAD_REQUEST)

       
        