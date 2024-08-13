from rest_framework.serializers import ModelSerializer
from .models import *

class EmployeeSerializer(ModelSerializer):
    
    class Meta:
        model = Employees
        fields="__all__"