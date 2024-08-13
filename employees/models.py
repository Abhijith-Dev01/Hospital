from django.db import models
from hospital_data.models import Hospital
from users.models import User
from department.models import Department

class Documnents(models.Model):
    degree_certificate = models.FileField(null=True,blank=True)
    experience_certificate =models.FileField(null=True,blank=True)
    
class Employees(Documnents):
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')]
    
    ROLE_CHOICES =[
        ('manager','Manager'),
        ('nurse','Nurse'),
        ('pharmist','Pharmist'),
        ('other_staffs','Other')
    ]
    employee_id = models.CharField(max_length=20,unique=True)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    salary = models.FloatField(null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False)
    date_of_birth = models.DateField(null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    role = models.CharField(max_length=5,choices=ROLE_CHOICES,null=False)

    def __str__(self):
        return f"{self.role}-{self.first_name} {self.last_name}"