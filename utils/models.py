from django.db import models

# Create your models here.

class SequenceNumber(models.Model):
    section_choices = [('DOC','Doctor'),
                       ('PTNT','patient'),
                       ('EMP','Employee'),
                       ('APNT','Appointment'),
                       ('STY','STAY'),
                       ('OPRT','Operation'),
                       ('BL','BILL')]
    section = models.CharField(choices=section_choices,max_length=4)
    number = models.CharField(max_length=6)