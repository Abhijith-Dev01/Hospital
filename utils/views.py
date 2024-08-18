import random 
from .models import *

def generate_sequence_number(section):
    while True:
        number = int(''.join([str(random.randint(0,9)) for i in range(5)]))
        sequence_number,created =SequenceNumber.objects.get_or_create(section=section,number=number)  
        if created is True:
            unique_id = str(section) + str(number)
            return unique_id
        else:
            continue
    
