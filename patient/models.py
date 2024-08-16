from django.db import models
from hospital_data.models import Hospital
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.patient_id})"