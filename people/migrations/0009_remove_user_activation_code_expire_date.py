# Generated by Django 2.1.3 on 2018-11-19 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0008_auto_20181119_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='activation_code_expire_date',
        ),
    ]
