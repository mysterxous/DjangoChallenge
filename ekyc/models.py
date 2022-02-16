import email
from email.headerregistry import Address
from types import CoroutineType
from django.db import models
from isort import code
# from django_countries.fields import CountryField
# from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import User
# Create your models here.
class Register(models.Model):
    
    birthday    = models.DateField()
    tel         = models.CharField("Tel /Phone",        max_length=12)
    address     = models.CharField("Address",           max_length=1024,)
    zip_code    = models.CharField("ZIP / Postal code", max_length=12,)
    city        = models.CharField("City",              max_length=1024,)
    country     = models.CharField("Country",           max_length=3,)
    file_id     = models.FileField("ID card file",)
    file_face   = models.FileField("Face file",)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    
    
    
    