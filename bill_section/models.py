from django.db import models
from medical_resources.models import Pharmacy 
from patient.models import Patient
from doctors.models import Doctor  
from hospital_data.models import Hospital

class PharmacyBill(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    bill_id = models.CharField(max_length=100, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    items = models.ManyToManyField(Pharmacy, through='PharmacyBillItem')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pharmacy Bill {self.bill_id} for {self.patient.first_name} {self.patient.last_name}"

class PharmacyBillItem(models.Model):
    pharmacy_bill = models.ForeignKey(PharmacyBill, on_delete=models.CASCADE)
    pharmacy_item = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.pharmacy_item.name} x {self.quantity}"

class OperationCost(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    operation_id = models.CharField(max_length=100, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=255)
    operation_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Operation Cost {self.operation_id} for {self.patient.first_name} {self.patient.last_name}"
    

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('general', 'General'),
        ('semi_private', 'Semi-Private'),
        ('private', 'Private'),
        ('icu', 'ICU'),
    ]
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()})"

class BedRestCost(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    stay_id = models.CharField(max_length=100, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bed Rest Cost {self.stay_id} for {self.patient.first_name} {self.patient.last_name} in Room {self.room.room_number}"