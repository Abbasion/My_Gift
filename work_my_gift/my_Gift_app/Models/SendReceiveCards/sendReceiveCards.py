from django.db import models
from django.utils import timezone

from my_Gift_app.Models.Cards.cards import Cards
from my_Gift_app.Models.Users.users import User


class SendReceiveCards(models.Model):
    Id = models.AutoField(primary_key=True)
    senderId = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    receiverPhone = models.TextField(default="",null=True,blank=True)
    isClaimed = models.BooleanField(default=False)
    cardPic = models.TextField(default="",null=True,blank=True)
    description = models.TextField(default="",null=True,blank=True)
    recieverName = models.TextField(default="",null=True,blank=True)
    creation_time = models.DateTimeField(default=timezone.now)
    isDeleted = models.BooleanField(default=False)