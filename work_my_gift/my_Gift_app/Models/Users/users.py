from __future__ import unicode_literals

from datetime import datetime

from django.db import models, transaction


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,BaseUserManager
)
class UserManager(BaseUserManager):

    def _create_user(self,Email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        print("createuser",Email)
        if not Email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(Email=Email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('isActive', True)
        extra_fields.setdefault('isDeleted', False)
        extra_fields.setdefault('Creation_Time',datetime.now())
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        print("super",email,password)
        extra_fields.setdefault('isActive', True)
        extra_fields.setdefault('isDeleted', False)
        extra_fields.setdefault('Creation_Time', datetime.now())
        extra_fields.setdefault('RoleType', 0)
        extra_fields.setdefault('RoleName', "Admin")

        return self._create_user(Email=email, password=password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    Id = models.AutoField(primary_key=True)
    UserName = models.TextField(blank=True,null=True)
    Email = models.EmailField(unique=True)
    PhoneNumber = models.CharField(blank=True,null=True,unique=True,max_length=40)
    Country = models.TextField(blank=True,null=True)
    RoleType =models.IntegerField(default=0)
    RoleName = models.TextField(default="Admin")
    Creation_Time = models.DateTimeField(default=timezone.now)
    Deletion_Time = models.DateTimeField(blank=True,null=True,default=None)
    profilePic = models.TextField(blank=True,default=None,null=True)
    isDeleted = models.BooleanField(blank=True,null=True,default=False)
    isActive = models.BooleanField(blank=True,null=True,default=True)
    isVerified = models.BooleanField(blank=True,null=True,default=False)
    isSocial = models.BooleanField(blank=True,null=True,default=False)
    address = models.TextField(blank=True,default=None,null=True)
    language = models.TextField(blank=True,default="English",null=True)
    objects = UserManager()


    USERNAME_FIELD = 'PhoneNumber'


    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self