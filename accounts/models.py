from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


#user registration model

class CustomUser(AbstractUser):
    mobile_phone = models.CharField(
        validators=[RegexValidator(regex=r'^01[0-2,5]{1}[0-9]{8}$', message="Enter a valid Egyptian phone number")],
        max_length=11,
        unique=True
    )
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    

