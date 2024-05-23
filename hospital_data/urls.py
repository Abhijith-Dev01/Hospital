from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

app_name="hospital_data"

router.register('hospital-data',HospitalViewset,basename='hospital-data')

urlpatterns=[path("",include(router.urls))]