from django.urls import path,include
from rest_framework import routers
from .views import * 
router = routers.DefaultRouter()
app_name = 'hospital/bills/'

router.register("",PharmacyBillViewSet,basename='bill')
router.register("operation-cost",OperationCostViewSet,basename='operation-cost')
router.register("bedrest-cost",BedRestCostViewSet,basename='bedrest-cost')
urlpatterns=[
            path('',include(router.urls))
]