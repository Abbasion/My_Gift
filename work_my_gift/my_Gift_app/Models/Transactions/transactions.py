from datetime import datetime

from django.db import models

from my_Gift_app.Models.Cards.cards import Cards
from my_Gift_app.Models.Users.users import User


class Transactions(models.Model):
    Id = models.AutoField(primary_key=True)
    order_ref = models.TextField(blank=True,null=True)
    cart_id = models.TextField(blank=True,null=True)
    amount = models.FloatField(blank=True,null=True)
    currency = models.TextField(blank=True,null=True)
    status_code = models.IntegerField(default=0)
    status_message = models.TextField(blank=True, null=True)
    payment_type = models.TextField(blank=True,null=True)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_to = models.TextField(blank=True,null=True)
    customer_name = models.TextField(blank=True,null=True)
    customer_email = models.EmailField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    card_id = models.ForeignKey(Cards,on_delete=models.CASCADE,blank=True,null=True)
    IBAN = models.TextField(blank=True,null=True)
    purpose = models.TextField(blank=True,null=True)
    country = models.TextField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    creation_time = models.DateTimeField(default=datetime.now)
    isDeleted = models.BooleanField(default=False)