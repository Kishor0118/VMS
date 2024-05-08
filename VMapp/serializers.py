from rest_framework import serializers
from .models import Vendor, Purchaseorder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchaseorder
        fields = '__all__'

    def create(self, validated_data):
        # Remove any problematic fields from validated_data
        validated_data.pop('non_valid_field', None)
        
        return Purchaseorder.objects.create(**validated_data)
