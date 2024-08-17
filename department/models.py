from django.db import models
from hospital_data.models import *
# Create your models here.
class  Department(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=4)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.hospital.code}-{self.name}"