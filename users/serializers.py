from rest_framework.serializers import ModelSerializer,CharField,EmailField,Serializer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import  PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import smart_str,smart_bytes,force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_norm_email
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegisterSerializer(ModelSerializer):
    password = CharField(max_length=68,min_length=8,write_only=True)
    password2 = CharField(max_length=68,min_length=8,write_only=True)
    
    class Meta:      
        model = User
        fields = ['username','password','email','password2','first_name','last_name']
        
    
    def validate(self,attrs):
        password = attrs.get('password','')
        password2 = attrs.get('password2','')
        if password != password2:
            raise ValidationError("Passwords do not match")
        
        return attrs
        
    def create(self,validated_data):
        user = User.objects.create_user(
                username=validated_data.get('username'),
                email=validated_data.get('email'),
                first_name=validated_data.get('first_name'),
                last_name= validated_data.get('last_name'),
                password= validated_data.get('password')
                
        )
        return user

class LoginSerializer(ModelSerializer):
    email = EmailField(max_length=255,min_length=6)
    password = CharField(max_length=255,write_only=True)
    full_name = CharField(max_length=255,read_only=True)
    access_token = CharField(max_length=255,read_only=True)
    refresh_token = CharField(max_length=255,read_only=True)
    
    class Meta:
        model=User
        fields =['email','password','full_name','access_token','refresh_token']
        
    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request,email=email,password=password)
        if not user:
            raise ValidationError("Invalida credentails ")
        user_tokens = user.tokens()
        
        return {
            "email":user.email,
            "full_name":user.get_full_name,
            "access_token":str(user_tokens.get('access')),
            "refresh_token":str(user_tokens.get('refresh'))
            }
        
class ResetPasswordSerializer(Serializer):
    email  = EmailField(max_length=255)
    
    class Meta:
        fields=['email']
        
    def validate(self,attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid64 = urlsafe_base64_encode(smart_bytes(user.id))
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user=user)   
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link = f'users/password-reset/password-reset-confirm/{uid64}/{token}'
            abs_link=f'http://{site_domain}{relative_link}'
            email_body = f'Hi use the link below to reset your password \n {abs_link}'
            data ={
                'email_body':email_body,
                'email_subject': 'Reset Your Password',
                'to_email':user.email
                
            }             
            send_norm_email(data)   
            
            return super().validate(attrs)     
        
class SetNewPasswordSerializer(Serializer):
    password = CharField(max_length=255,min_length=6,write_only=True)
    confirm_password = CharField(max_length=255,min_length=6,write_only=True)
    uidb64 = CharField(write_only=True)
    token = CharField(write_only=True)
    
    class Meta:
        fields=['password','confirm_password','uidb64','token']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user=user,token=token):
                raise ValidationError("reset link is invalid or expired")
            
            if password !=confirm_password:
                raise ValidationError("passwords doesnot match")
            
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise ValidationError(str(e))
            
class LogoutSerializer(Serializer):
    refresh_token = CharField(write_only=True)
    
    def validate(self,attrs):
        self.token = attrs.get('refresh_token')
        return attrs
    
    
    def save(self ,*kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
            
        except Exception as e:
             raise ValidationError(str(e))
            