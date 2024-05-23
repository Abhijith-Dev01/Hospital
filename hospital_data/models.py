from django.db import models

class Location(models.Model):
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    
class Hospital(Location):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=4,unique=True)
    branch = models.CharField(max_length=50)


    