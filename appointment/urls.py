from django.urls import path,include
from rest_framework import routers
from .views import * 
router = routers.DefaultRouter()
app_name = 'hospital/appointment'

router.register("",AppointmentViewSet,basename='appointment')
urlpatterns=[
            path('',include(router.urls))
]