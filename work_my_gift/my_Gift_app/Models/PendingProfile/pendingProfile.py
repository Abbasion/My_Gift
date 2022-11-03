from django.db import models


from django.utils import timezone

from my_Gift_app.Models.Users.users import User


class PendingProfile(models.Model):
    Id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    UserName = models.TextField(blank=True,null=True)
    Email = models.EmailField(unique=True)
    PhoneNumber = models.TextField(blank=True,null=True)
    Country = models.TextField(blank=True,null=True)
    Creation_Time = models.DateTimeField(default=timezone.now)
    Deletion_Time = models.DateTimeField(blank=True,null=True,default=None)
    profilePic = models.TextField(blank=True,default=None,null=True)
    isDeleted = models.BooleanField(blank=True,null=True,default=False)
    address = models.TextField(blank=True,default=None,null=True)
    status = models.IntegerField(default=0)