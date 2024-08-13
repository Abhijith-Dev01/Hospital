from django.db import models
from hospital_data.models import Hospital
from department.models import Department
class Equipment(models.Model):
    EQUIPMENT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Maintenance'),
        ('out_of_service', 'Out of Service'),
    ]
    
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    equipment_id = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    status = models.CharField(max_length=20, choices=EQUIPMENT_STATUS_CHOICES, default='available')
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}-{self.equipment_id})"
    

class Pharmacy(models.Model):
    MEDICINE_TYPE_CHOICES = [
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('ointment', 'Ointment'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    medicine_id = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=MEDICINE_TYPE_CHOICES)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=255)
    quantity_in_stock = models.IntegerField()
    expiry_date = models.DateField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} (ID: {self.medicine_id})"