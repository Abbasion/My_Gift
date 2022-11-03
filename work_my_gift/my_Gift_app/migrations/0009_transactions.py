# Generated by Django 4.1.2 on 2022-10-28 13:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_Gift_app', '0008_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('order_ref', models.TextField(blank=True, null=True)),
                ('cart_id', models.TextField(blank=True, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('currency', models.TextField(blank=True, null=True)),
                ('status_code', models.IntegerField(default=0)),
                ('status_message', models.TextField(blank=True, null=True)),
                ('payment_type', models.TextField(blank=True, null=True)),
                ('sent_to', models.TextField(blank=True, null=True)),
                ('customer_name', models.TextField(blank=True, null=True)),
                ('customer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('IBAN', models.TextField(blank=True, null=True)),
                ('purpose', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('creation_time', models.DateTimeField(default=datetime.datetime.now)),
                ('isDeleted', models.BooleanField(default=False)),
                ('card_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_Gift_app.cards')),
                ('sent_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]