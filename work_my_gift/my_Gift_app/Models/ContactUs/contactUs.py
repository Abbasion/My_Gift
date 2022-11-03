from django.db import models

from django.utils import timezone
class ContactUs(models.Model):
    Id = models.AutoField(primary_key=True)
    name= models.TextField(default="",null=True,blank=True)
    email = models.EmailField(default="",null=True,blank=True)
    phoneNumber = models.TextField(default="",null=True,blank=True)
    message = models.TextField(default="",null=True,blank=True)
    creation_time = models.DateTimeField(default=timezone.now)
    isDeleted = models.BooleanField(default=False)