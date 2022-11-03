from django.db import models


class AdminWallet(models.Model):
    Id = models.AutoField(primary_key=True)
    balance = models.TextField(default="",null=True,blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)