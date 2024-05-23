from django.urls import path,include
from rest_framework import routers
from .views import *
# Overall, using routers in Django REST Framework helps streamline 
# the development process, improve code organization, and
# maintain consistency in your API design.
# Automatic URL Routing
# Consistent URL Patterns
# Simplified Viewset Registration
# Support for Nested Routes
# Default Naming Conventions
# Easier Maintenance


router  = routers.DefaultRouter()
app_name= "hospital/department"

router.register("",DepartmentViewSet,basename="department")
urlpatterns=[
            path('',include(router.urls))
]

