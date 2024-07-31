from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,\
                                        Group,Permission)
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True,verbose_name=_("Email Address"))
    username = models.CharField(max_length=255,unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name']
    
    # Specify unique related_name values
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Avoid conflicts with the default User model
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Avoid conflicts with the default User model
        blank=True,
    )
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.username}"

    def get_full_name(self):
        return f"{self.first_name}-{self.last_name}"
    
    @property
    def tokens(self):
        pass