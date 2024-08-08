from django.urls import path,include
from rest_framework import routers
from .views import *



router  = routers.DefaultRouter()
app_name= "users"

router.register("register",UserRegisterViewset,basename="register")
router.register("login",LoginUserViewSet,basename="login")
router.register("password-reset",PasswordResetViewSet,basename="password-reset")
router.register("set-new-password",SetNewPasswordViewSet,basename="set-new-password")
router.register('logout',LogoutViewSet,basename='logout')
urlpatterns=[
                path('',include(router.urls))
            ]