from .serializers  import UserRegisterSerializer,LoginSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework import status,pagination
from rest_framework.response import Response
from .utils import send_otp
from .models import *
from django.core.exceptions import ValidationError
from rest_framework.decorators import action

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
            
    
    @transaction.atomic
    @action(methods=['POST'],detail=False,url_path='verify-otp',url_name='verify-otp')
    def verify_otp(self,request):
        otp = request.data.get('otp',None)
        if otp is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,data="otp is required")
        otp_data = OneTimePassword.objects.get(otp=otp)
        if not otp_data.user.is_verified:
            otp_data.user.is_verified = True
            otp_data.user.save()
        else:
             return Response(status=status.HTTP_400_BAD_REQUEST,data="otp is already verified")
        
        return Response(status=status.HTTP_200_OK,
                        data={"message":"OTP verification done successfully"})

class LoginUserView(ModelViewSet):
    serializer_class=LoginSerializer
    
    def create(self,request):
            serializer = self.serializer_class(data=request.data,
                                               context={'request':request})
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        
        