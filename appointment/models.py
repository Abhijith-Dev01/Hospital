from hospital_data.models import * 
from patient.models import *
from doctors.models import *
# Create your models here.
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    appointment_id = models.CharField(max_length=100, unique=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    appointment_fees = models.FloatField(null=True,blank=True)
    reason_for_visit = models.TextField()
    appointment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    prescription = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.patient.first_name} {self.patient.last_name} with Dr. {self.doctor.last_name}"