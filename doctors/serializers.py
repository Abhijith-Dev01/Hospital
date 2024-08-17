from rest_framework.serializers import ModelSerializer
from .models import *

class DoctorSerializer(ModelSerializer):
    
    class Meta:
        model = Doctor
        fields = "__all__"