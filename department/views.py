from . models import Department
from rest_framework.viewsets import ModelViewSet
from rest_framework import status,pagination
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from .serializers import DepartmentSerializer
from django.db.models import F
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
class DepartmentPagination(pagination.PageNumberPagination):
    page_size = 50
    max_page_size = 1000


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all().order_by('-id')
    pagination_class = DepartmentPagination


    
    def list(self,request):
        response_data = list(self.queryset.values().annotate(hospital_name=F('hospital__name'),
                                                             hospital_code=F('hospital__code')))
        return Response(data=response_data,status=status.HTTP_200_OK)
    
    @transaction.atomic
    def create(self,request):
        request_data = request.data
        serializer = DepartmentSerializer(data=request_data,many=True)
        new_data =[]
        for data in request_data:
            department_qs = list(self.queryset.filter(code=data['code'],
                                                    hospital=data['hospital']))

            if len(department_qs) ==0:
                new_data.append(data)
        
        request_data = new_data
        if len(request_data)>0:
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED, data={
                                    "message":"Department created successfully"})
        else:
            raise ValidationError({"error":"Department with this code already exist in this hospital"})