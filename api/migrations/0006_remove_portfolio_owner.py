# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-07 06:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20171207_0625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='owner',
        ),
    ]
