from django.urls import path,include
from rest_framework import routers
from .views import * 
router = routers.DefaultRouter()
app_name = 'hospital/employees'

router.register("",EmployeeViewSet,basename='employees')
urlpatterns=[
            path('',include(router.urls))
]