from django.db import models
from hospital_data.models import Hospital
from users.models import User
from department.models import Department

class Documnents(models.Model):
    degree_certificate = models.FileField(null=True,blank=True)
    experience_certificate =models.FileField(null=True,blank=True)
    
class Doctor(Documnents):
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')]
    
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    salary = models.FloatField(null=False)
    specialization = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False)
    date_of_birth = models.DateField(null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    doctor_id = models.CharField(max_length=25,unique=True)


    def __str__(self):
        return f"{self.specialization}-{self.first_name} {self.last_name}"