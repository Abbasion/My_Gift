from django.db import models


from django.utils import timezone

from my_Gift_app.Models.Users.users import User


class Cards(models.Model):
    Id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.TextField(default="",null=True,blank=True)
    amount = models.TextField(default="",null=True,blank=True)
    description = models.TextField(default="",null=True,blank=True)
    deduction = models.TextField(default="",null=True,blank=True)
    color = models.TextField(default="",null=True,blank=True)
    background_color = models.TextField(default="",null=True,blank=True)
    creation_time = models.DateTimeField(default=timezone.now)
    isDeleted = models.BooleanField(default=False)