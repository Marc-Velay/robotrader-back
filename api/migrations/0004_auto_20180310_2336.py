# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-10 23:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180310_2150'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candles',
            old_name='name',
            new_name='item',
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=10),
        ),
    ]