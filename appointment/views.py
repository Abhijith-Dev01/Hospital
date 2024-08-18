
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from . models import *
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from rest_framework import status,response
from django.db.models import F,Value
from rest_framework.decorators import action
from rest_framework.validators import ValidationError
from utils.views import generate_sequence_number
from django.db.models.functions import Concat
# Create your views here.

class AppointmentPagination(PageNumberPagination):
    page_size=50
    max_page_size=1000
    
    
class AppointmentViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Appointment.objects.all()
    pagination_class=AppointmentPagination
    serializer_class = AppointmentSerializer
    
    def create(self,request):
        request_data = request.data
        new_data =[]
        for data in request_data:
                appointment_qs = list(self.queryset.filter(patient=data['patient'],
                                                        doctor = data['doctor'],
                                                        appointment_status='scheduled',
                                                    hospital=data['hospital']))

                if len(appointment_qs) ==0:
                    data['appointment_id'] = generate_sequence_number('APNT')
                    new_data.append(data)
        
        request_data = new_data
        if request_data is not None and len(request_data)>0:
            serializer = self.serializer_class(data=request_data,many=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(status=status.HTTP_201_CREATED, data={
                                        "message":"Appointment scheduled successfully"})
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                    "message": "Invalid data",
                    "errors": serializer.errors
                })
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={
                                            "message":"Invalid/Empty data"})
       
            
    def list(self,request):

        appointment_list = list(self.queryset.values().annotate(
                            hospital__name= F('hospital__name'),
                            doctor__name = F('doctor__first_name'),
                            doctor_id = F('doctor__doctor_id'),
                            patient_name =Concat(F('patient__first_name'),Value('-'),F('patient__last_name'))
        ))
        return response.Response(status=status.HTTP_200_OK,
                                 data=appointment_list)  
        
    @action(methods=['PATCH'],detail=True,url_name='cancel_appointment',url_path='cancel_appointment')
    def cancel_appointment(self,request,pk):
        try:
            self.queryset.filter(id=pk).update(appointment_status="cancelled")
            appointment_id = self.queryset.get(id=id).appointment_id
        except Exception as e:
            raise ValidationError(str(e))
        
        return response.Response(status=status.HTTP_200_OK,
                                 data={"message":f"appointment {appointment_id} is cancelled"})
    
    @action(methods=['PATCH'],detail=True,url_name='cancel_appointment',url_path='cancel_appointment')
    def cancel_appointment(self,request,pk):
        try:
            self.queryset.filter(id=pk).update(appointment_status="cancelled")
            appointment_id = self.queryset.get(id=id).appointment_id
        except Exception as e:
            raise ValidationError(str(e))
        
        return response.Response(status=status.HTTP_200_OK,
                                 data={"message":f"appointment {appointment_id} is cancelled"})
    
    @action(methods=['PATCH'],detail=False,url_name='appointment_completed',url_path='appointment_completed')
    def appointment_completed(self,request,):
        try:
            id_list = request.data['appointment_id']
            self.queryset.filter(appointment_id__in=id_list).update(appointment_status="completed")
            appointment_id = self.queryset.get(id=id).appointment_id
        except Exception as e:
            raise ValidationError(str(e))
        
        return response.Response(status=status.HTTP_200_OK,
                                 data={"message":f"appointment {appointment_id} is appointment_completed"})