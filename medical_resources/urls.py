from django.urls import path,include
from rest_framework import routers
from .views import * 
router = routers.DefaultRouter()
app_name = 'hospital/resources/'

router.register("pharmacy",PharmacyViewSet,basename='pharmacy')
router.register("equipment",EquipmentViewSet,basename='equipment')
urlpatterns=[
            path('',include(router.urls))
]