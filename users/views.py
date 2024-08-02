from .serializers  import UserRegisterSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework import status,pagination
from rest_framework.response import Response
from .utils import send_otp
from .models import *
from django.core.exceptions import ValidationError
class UserPagination(pagination.PageNumberPagination):
    page_size =100
    max_page_size=1000
    
    
class UserRegisterViewset(ModelViewSet):
    serializer_class=UserRegisterSerializer
    queryset = User.objects.all()
    pagination_class=UserPagination
    
    @transaction.atomic
    def create(self,request):
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            send_otp(user_data['email'])
            return Response(status=status.HTTP_200_OK,
                data={'data':user_data,
                      'message':f"Hi {user_data['first_name']} thanks for signing up ;A passcode is send to your email"
                      })
            
        return Response(status=status.HTTP_400_BAD_REQUEST,data=serializer.errors)
            
            
    