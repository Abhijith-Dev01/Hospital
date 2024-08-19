from django.contrib import admin
from .models import *

admin.site.register(PharmacyBill)
admin.site.register(PharmacyBillItem)
admin.site.register(OperationCost)
admin.site.register(Room)
admin.site.register(BedRestCost)