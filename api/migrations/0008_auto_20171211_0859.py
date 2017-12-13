# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-11 08:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0007_portfolio_owner'),
    ]

    operations = [

        migrations.RemoveField(
            model_name='portfolio',
            name='owner',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='item',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to='api.Item'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to=settings.AUTH_USER_MODEL),
        ),
        
    ]
