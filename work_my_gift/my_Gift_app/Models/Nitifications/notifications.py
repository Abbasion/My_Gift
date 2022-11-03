from django.db import models


from django.utils import timezone

from my_Gift_app.Models.Users.users import User


class Notifications(models.Model):
    Id = models.AutoField(primary_key=True)
    notification_by = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_to = models.TextField(default="", null=True, blank=True)
    description = models.TextField(default="", null=True, blank=True)
    read = models.BooleanField(default=False)
    unread = models.BooleanField(default=True)
    creation_time = models.DateTimeField(default=timezone.now)
    isDeleted = models.BooleanField(default=False)