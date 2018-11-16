# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-16 17:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_auto_20181113_1356'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherFreeTimes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='زمان شروع')),
                ('end', models.TimeField(verbose_name='ساعت پایان')),
                ('student_capacity', models.IntegerField(verbose_name='ظرفیت')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Teacher', verbose_name='استاد')),
            ],
        ),
    ]
