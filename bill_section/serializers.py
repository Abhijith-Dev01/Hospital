from rest_framework.serializers import ModelSerializer
from .models import *

class PharmacyBillSerializer(ModelSerializer):
    
    class Meta:
        model = PharmacyBill
        fields="__all__"
        

class OperationSerializer(ModelSerializer):
    
    class Meta:
        model = OperationCost
        fields="__all__"
        
        
class BedRestSerializer(ModelSerializer):
    
    class Meta:
        model = BedRestCost
        fields="__all__"