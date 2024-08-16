from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from . models import *
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from rest_framework import status,response
from django.db.models import F
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
        pharmacy_bill_list = list(self.queryset.values().annotate(
                            hospital__name= F('hospital__name'), 
        ))
        return response.Response(status=status.HTTP_200_OK,
                                 data=pharmacy_bill_list)  
        
        
class OperationCostViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = OperationCost.objects.all()
    pagination_class=BillPagination
    serializer_class = OperationSerializer
    
    def create(self,request):
        request_data = request.data
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
                            hospital__name= F('hospital__name'), 
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
        ))
        return response.Response(status=status.HTTP_200_OK,
                                 data=bed_rest_bill_list)  