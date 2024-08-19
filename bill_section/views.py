from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from . models import *
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from rest_framework import status,response
from django.db.models import F,Value
from utils.views import generate_sequence_number
from django.db.models.functions import Concat
# Create your views here.

class BillPagination(PageNumberPagination):
    page_size=50
    max_page_size=1000
    
class PharmacyBillViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = PharmacyBill.objects.all()
    pagination_class=BillPagination
    serializer_class = PharmacyBillSerializer
    
    def create(self,request):
        request_data = request.data
        for data in request_data:
            data['bill_id'] = generate_sequence_number('BL') 
            
        if request_data is not None and len(request_data)>0:
            serializer = self.serializer_class(data=request_data,many=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(status=status.HTTP_201_CREATED, data={
                                        "message":"Pharmacy bills generated successfully"})
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                    "message": "Invalid data",
                    "errors": serializer.errors
                })
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                                        "message":"Invalid/Empty data"})
   
            
    def list(self,request):
        pharmacy_bill_list = list(PharmacyBill.objects.values().annotate(
                             hospital_name= F('hospital__name'), 
                             patient_name = Concat(F('patient__first_name'),Value('-'),F('patient__last_name')),
                            
        ))
        pharmacy_bill_item_list = list(PharmacyBillItem.objects.values().annotate(
                                        medicine_name = F('pharmacy_item__name')
        ))
        for data in pharmacy_bill_list:
            item_list = []
            for item in pharmacy_bill_item_list:
                if data['id'] == item['pharmacy_bill_id']:
                    item_list.append(item)
                else:
                    continue
            data['items'] = item_list
                
        return response.Response(status=status.HTTP_200_OK,
                                 data=pharmacy_bill_list)  
        
        
class OperationCostViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = OperationCost.objects.all()
    pagination_class=BillPagination
    serializer_class = OperationSerializer
    
    def create(self,request):
        request_data = request.data
        for data in request_data:
            data['operation_id'] = generate_sequence_number('OPRT') 
        if request_data is not None and len(request_data)>0:
            serializer = self.serializer_class(data=request_data,many=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(status=status.HTTP_201_CREATED, data={
                                        "message":"Operation Cost bills generated successfully"})
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                    "message": "Invalid data",
                    "errors": serializer.errors
                })
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                                        "message":"Invalid/Empty data"})
   
            
    def list(self,request):
        operation_bill_list = list(self.queryset.values().annotate(
                            hospital_name= F('hospital__name'), 
                            patient_name = Concat(F('patient__first_name'),Value('-'),F('patient__last_name')),
                            doctor_name= Concat(F('doctor__first_name'),Value('-'),F('doctor__last_name'))
        ))
        return response.Response(status=status.HTTP_200_OK,
                                 data=operation_bill_list)  
        

class BedRestCostViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = BedRestCost.objects.all()
    pagination_class=BillPagination
    serializer_class = BedRestSerializer
    
    def create(self,request):
        request_data = request.data
        for data in request_data:
            data['stay_id'] = generate_sequence_number('STY') 
            data['room']['hospital'] = data['hospital']

        if request_data is not None and len(request_data)>0:
            serializer = self.serializer_class(data=request_data,many=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(status=status.HTTP_201_CREATED, data={
                                        "message":"Bed rest  bills generated successfully"})
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                    "message": "Invalid data",
                    "errors": serializer.errors
                })
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                                        "message":"Invalid/Empty data"})
   
            
    def list(self,request):
        bed_rest_bill_list = list(self.queryset.values().annotate(
                            hospital__name= F('hospital__name'),
                            patient_name = Concat(F('patient__first_name'),Value('-'),F('patient__last_name')),
                            room_number = F('room__room_number'),
                            room_type = F('room__room_type')
                             
        ))
        return response.Response(status=status.HTTP_200_OK,
                                 data=bed_rest_bill_list)  