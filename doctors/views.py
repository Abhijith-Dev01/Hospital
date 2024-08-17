from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from . models import *
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from rest_framework import status,response
from django.db.models import F
from utils.views import generate_sequence_number
from django.db import transaction
# Create your views here.

class DoctorPagination(PageNumberPagination):
    page_size=50
    max_page_size=1000
class DoctorViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Doctor.objects.all()
    pagination_class=DoctorPagination
    serializer_class = DoctorSerializer
    
    @transaction.atomic
    def create(self,request):
        request_data = request.data
        username = request.user
        user_info = User.objects.get(username=username)
        if user_info.is_manager is True:
            new_data =[]
            for data in request_data:
                doctor_qs = list(self.queryset.filter(email=data['email'],
                                                    hospital=data['hospital']))

                if len(doctor_qs) ==0:
                    data['doctor_id'] = generate_sequence_number('DOC')
                    new_data.append(data)
        
            request_data = new_data
    
            if request_data is not None and len(request_data)>0:
                serializer = self.serializer_class(data=request_data,many=True)
                if serializer.is_valid():
                    serializer.save()
                    return response.Response(status=status.HTTP_201_CREATED, data={
                                            "message":"Doctor data created successfully"})
                else:
                    return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                        "message": "Invalid data",
                        "errors": serializer.errors
                    })
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                                            "message":"Invalid/Empty/repeated  data"  })
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                                            "message":"Logged in user has no permission to create doctors"})
            
    def list(self,request):
        username = request.user
        user = User.objects.get(username=username)
        if user.is_manager is True:
            doctor_list = list(self.queryset.values().annotate(
                                hospital_name= F('hospital__name'),
                                hospital_code = F('hospital__code'),
                                department_name =F('department__name'),
            ))
        else:
            value_fields = ['first_name','last_name','email','specialization','degree',
                            'gender']
            doctor_list = list(self.queryset.values(*value_fields).annotate(
                                hospital_name= F('hospital__name'),
                                hospital_code = F('hospital__code'),
                                department_name =F('department__name'),
            ))
        return response.Response(status=status.HTTP_200_OK,
                                 data=doctor_list)  