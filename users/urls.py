from django.urls import path,include
from rest_framework import routers
from .views import *



router  = routers.DefaultRouter()
app_name= "hospital/users"

router.register("users",UserViewset,basename="users")
urlpatterns=[
                path('',include(router.urls))
            ]