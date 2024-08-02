import random
from django.core.mail import EmailMessage
from hospital import settings
from .models import *

def generateOtp():
    otp =''
    for i in range(6):
        otp += str(random.randint(1,9))
    
    return otp

def send_otp(email):
    Subject = "One time code for email verification"
    otp_code = generateOtp()
    user = User.objects.get(email=email)
    email_body = f"Hi {user.first_name}, thanks for signing up please verify your email using the given one time password {otp_code}"
    from_email = settings.EMAIL_HOST_USER
    
    OneTimePassword.objects.create(user=user,otp=otp_code)
    send_email = EmailMessage(subject=Subject,body=email_body,from_email=from_email,
                              to=[email])
    send_email.send()
    
    