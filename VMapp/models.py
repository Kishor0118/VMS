from django.db import models
from django.utils import timezone
from django.db.models import Avg
from django.db.models import F
from django.dispatch import receiver
from django.db.models.signals import post_save

class Vendor(models.Model):
    vendor_code = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Purchaseorder(models.Model):
    po_number = models.CharField(max_length=50, unique=True, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    
class Historicalperformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"  
    
@receiver(post_save, sender=Purchaseorder)
def vendorperformance(sender, instance, **kwargs):
    if instance.status == 'Complete' and instance.delivery_date is None:
        instance.delivery_date = timezone.now()
        instance.save()   
         
    # On Time Delivery Rate
    completeorders = Purchaseorder.objects.filter(vendor=instance.vendor, status='Complete')
    on_time_deliveries = completeorders.filter(delivery_date__gte=F('delivery_date'))
    on_time_delivery_rate = on_time_deliveries.count() / completeorders.count()
    instance.vendor.on_time_delivery_rate = on_time_delivery_rate if on_time_delivery_rate else 0
    
    # Quality Rating Average
    completeorders_with_rating = completeorders.exclude(quality_rating__isnull=True)
    quality_rating_avg = completeorders_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
    instance.vendor.quality_rating_avg = quality_rating_avg if quality_rating_avg else 0
    instance.vendor.save()
    

@receiver(post_save, sender=Purchaseorder)
def update_response_time(sender, instance, **kwargs):
    
    # Update Average Response Time
    responsetimes = Purchaseorder.objects.filter(vendor=instance.vendor, acknowledgment_date__isnull=False).values_list('acknowledgment_date','issue_date')
    average_response_time = sum((acknowledgment_date - issue_date ).total_seconds() for acknowledgment_date, issue_date in responsetimes)
    if average_response_time < 0:
        average_response_time = 0
    if responsetimes:
        average_response_time = average_response_time / len(responsetimes)
    else:
        average_response_time = 0  
    instance.vendor.average_response_time = average_response_time
    instance.vendor.save()    

@receiver(post_save, sender=Purchaseorder)
def update_fulfillment_rate(sender, instance, **kwargs):
    # Update Fulfillment Rate
    fulfilled_orders = Purchaseorder.objects.filter(vendor=instance.vendor, status='complete')  
    fulfillment_rate = fulfilled_orders.count() / Purchaseorder.objects.filter(vendor=instance.vendor).count()
    instance.vendor.fulfillment_rate = fulfillment_rate
    instance.vendor.save()      