from rest_framework import status,viewsets,pagination
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from .serializers import * 
from django.db.models import F
from rest_framework.permissions import IsAuthenticated
class HospitalPagination(pagination.PageNumberPagination):
    page_size =100
    max_page_size=1000
    
class HospitalViewset(viewsets.ModelViewSet):
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all().order_by("-id")
    pagination_class = HospitalPagination
    permission_classes = [IsAuthenticated]
    

    def create(self,request):
        request_data = request.data
        serializer = HospitalSerializer(data=request_data, many=True)
        code_list= []
        for data in request_data:
            hospital_instance = Hospital.objects.filter(code=data['code'])
            if len(hospital_instance)>0:
                code_list.append(data['code'])
                del data
        if len(request_data)>0:
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED, data={
                                    "message":"Hospital created successfully"})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        else:
            raise ValidationError(f"Hospital already existed with codes {code_list}")
        
    