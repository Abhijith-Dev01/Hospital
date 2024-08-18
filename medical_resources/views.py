from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from . models import *
from rest_framework.pagination import PageNumberPagination
from .serailizers import *
from rest_framework import status,response
from django.db.models import F
from users.models import *
from utils.views import generate_sequence_number
# Create your views here.

class ResourcePagination(PageNumberPagination):
    page_size=50
    max_page_size=1000
    
    
class EquipmentViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Equipment.objects.all()
    pagination_class=ResourcePagination
    serializer_class = EquipmentSerializer
    
    def create(self,request):
        request_data = request.data
        username = request.user
        user_info = User.objects.get(username=username)
        if user_info.is_manager is True:
            new_data =[]
            for data in request_data:
                equipment_qs = list(self.queryset.filter(name=data['name'],
                                                    hospital=data['hospital']))

                if len(equipment_qs) ==0:
                    data['equipment_id'] = generate_sequence_number('EQP')
                    new_data.append(data)
        
            request_data = new_data
            if request_data is not None and len(request_data)>0:
                serializer = self.serializer_class(data=request_data,many=True)
                if serializer.is_valid():
                    serializer.save()
                    return response.Response(status=status.HTTP_201_CREATED, data={
                                            "message":"Equipment data created successfully"})
                else:
                    return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                        "message": "Invalid data",
                        "errors": serializer.errors
                    })
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                                            "message":"Invalid/Empty data"})
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                                            "message":"Logged in user has no permission to create equipments"})
            
    def list(self,request):
        username = request.user
        user_info = User.objects.get(username=username)
        if user_info.is_manager is True:
            equipment_list = list(self.queryset.values().annotate(
                                hospital__name= F('hospital__name'),
                                department__name =F('department__name') 
            ))
        else:
            value_fields =['name','equipment_id','description','last_maintenance_date',
                           'purchase_date','status','next_maintenance_date']
            equipment_list = list(self.queryset.values(*value_fields).annotate(
                                hospital__name= F('hospital__name'),
                                department__name =F('department__name') 
            ))
        return response.Response(status=status.HTTP_200_OK,
                                 data=equipment_list)  
        
        

    
class PharmacyViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Pharmacy.objects.all()
    pagination_class=ResourcePagination
    serializer_class = PharmacySerializer
    
    def create(self,request):
        request_data = request.data
        username = request.user
        user_info = User.objects.get(username=username)
        if user_info.is_manager is True:
            new_data =[]
            for data in request_data:
                pharmacy_qs = list(self.queryset.filter(name=data['name'],
                                                    hospital=data['hospital']))

                if len(pharmacy_qs) ==0:
                    data['medicine_id'] = generate_sequence_number('MDC')
                    new_data.append(data)
        
            request_data = new_data
            if request_data is not None and len(request_data)>0:
                serializer = self.serializer_class(data=request_data,many=True)
                if serializer.is_valid():
                    serializer.save()
                    return response.Response(status=status.HTTP_201_CREATED, data={
                                            "message":"Pharmacy data created successfully"})
                else:
                    return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                        "message": "Invalid data",
                        "errors": serializer.errors
                    })
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                                            "message":"Invalid/Empty data"})
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                                            "message":"Logged in user has no permission to create pharmacy products"})
            
