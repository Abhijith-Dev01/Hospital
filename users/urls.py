from django.urls import path,include
from rest_framework import routers
from .views import *



router  = routers.DefaultRouter()
app_name= "users"

router.register("register",UserRegisterViewset,basename="register")
urlpatterns=[
                path('',include(router.urls))
            ]