from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from . models import *
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from rest_framework import status,response
from django.db.models import F
# Create your views here.

class PatientPagination(PageNumberPagination):
    page_size=50
    max_page_size=1000
class PatientViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Patient.objects.all()
    pagination_class=PatientPagination
    serializer_class = PatientSerializer
    
    def create(self,request):
        request_data = request.data
        if request_data is not None and len(request_data)>0:
            serializer = self.serializer_class(data=request_data,many=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(status=status.HTTP_201_CREATED, data={
                                        "message":"Patient data created successfully"})
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                    "message": "Invalid data",
                    "errors": serializer.errors
                })
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                                        "message":"Invalid/Empty data"})
   
            
    def list(self,request):
        Patient_list = list(self.queryset.values().annotate(
                            hospital__name= F('hospital__name'),
        ))
        return response.Response(status=status.HTTP_200_OK,
                                 data=Patient_list)  