from rest_framework.serializers import ModelSerializer,CharField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *
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
