# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-17 14:32
from __future__ import unicode_literals

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=markdownx.models.MarkdownxField(blank=True, default='', max_length=500, verbose_name='زندگی نامه'),
        ),
    ]
