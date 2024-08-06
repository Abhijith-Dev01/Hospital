from rest_framework.serializers import ModelSerializer,CharField,EmailField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth import authenticate

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