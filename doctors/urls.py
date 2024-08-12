from django.urls import path,include
from rest_framework import routers
from .views import * 
router = routers.DefaultRouter()
app_name = 'hospital/doctors'

router.register("",DoctorViewSet,basename='doctors')
urlpatterns=[
            path('',include(router.urls))
]

