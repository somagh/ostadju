# Generated by Django 2.1.3 on 2018-11-19 14:31

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activation_code',
            field=models.UUIDField(default=uuid.uuid1),
        ),
        migrations.AddField(
            model_name='user',
            name='activation_code_expire_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 19, 14, 31, 7, 761842)),
        ),
    ]
