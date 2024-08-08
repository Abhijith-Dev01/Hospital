from .serializers  import *
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework import status,pagination
from rest_framework.response import Response
from .utils import send_otp
from .models import *
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated

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

class LoginUserViewSet(ModelViewSet):
    serializer_class=LoginSerializer
    
    def create(self,request):
            serializer = self.serializer_class(data=request.data,
                                               context={'request':request})
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        

class PasswordResetViewSet(ModelViewSet):
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()
    def create(self,request):
        serializer  = self.serializer_class(data=request.data,
                                            context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(data={"message":"A password reset link is send to your email"},status=status.HTTP_200_OK)

    @action(methods=['GET'],detail=False,url_name='password-reset-confirm',
            url_path='password-reset-confirm')
    def confirm_password_reset(self,request):
        try:
            uidb64= request.GET.get('uidb64')
            token = request.GET.get('token')
            user_id =smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'message':'token is invalid or has expired'})
            
            return Response(status=status.HTTP_200_OK,
                data={'message':'token is valid','uidb64':uidb64,'token':token})
            
        except Exception as e:
            raise ValidationError(str(e))


class SetNewPasswordViewSet(ModelViewSet):
    serializer_class=SetNewPasswordSerializer
    
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK,
                data={'message':'new password is successfully set'})


class LogoutViewSet(ModelViewSet):
    serializer_class=LoginSerializer
    permission_classes=[IsAuthenticated]
    
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK,
                        data= {"message":"you are logged out"})