from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
class UserManager(BaseUserManager):
    def email_validator(self,email):
        try:
            validate_email(email)
        except Exception as e:
            raise ValidationError(str(e))
        
    def create_user(self,email,first_name,last_name,password,**extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
            
        else:
            raise ValidationError('Email field is required')
        
        if not first_name:
            raise ValidationError('First Name is required')
        
        if not last_name:
            raise ValidationError('Last Name is required')
        
        user = self.model(email=email,first_name=first_name,last_name=last_name,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self,first_name,last_name,email,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_supervisor', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValidationError("is_staff variable must be true for admin user")
        if extra_fields.get('is_supervisor') is not True:
            raise ValidationError("is_supervisor variable must be true for admin user")
        
        
        user = self.create(email=email,first_name=first_name,last_name=last_name,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        
        return user