from rest_framework.serializers import ModelSerializer
from .models import *

class EquipmentSerializer(ModelSerializer):
    
    class Meta:
        model = Equipment
        fields = "__all__"
        
class PharmacySerializer(ModelSerializer):
    
    class Meta:
        model = Pharmacy
        fields = "__all__"