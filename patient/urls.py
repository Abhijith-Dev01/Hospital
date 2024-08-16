from django.urls import path,include
from rest_framework import routers
from .views import * 
router = routers.DefaultRouter()
app_name = 'hospital/patient'

router.register("",PatientViewSet,basename='patients')
urlpatterns=[
            path('',include(router.urls))
]
