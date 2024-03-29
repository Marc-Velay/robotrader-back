# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

# Stock and item model
class Item(models.Model):
    """
    All items
    """
    name = models.CharField(max_length = 10)
    source = models.CharField(max_length = 30)
    inst_type = models.CharField(max_length = 30)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

# Candlesticks model
class Candles(models.Model):
    """
    Candlesticks model
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False)
    timestamp = models.IntegerField()
    opening = models.DecimalField(max_digits=20,decimal_places=10)
    high = models.DecimalField(max_digits=20,decimal_places=10)
    low = models.DecimalField(max_digits=20,decimal_places=10)
    closing =  models.DecimalField(max_digits=20,decimal_places=10)
    volume =  models.DecimalField(max_digits=20,decimal_places=10)

# Predictions model
class Predictions(models.Model):
    """
    Predictions model
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False)
    timestamp = models.IntegerField()
    closing =  models.DecimalField(max_digits=20,decimal_places=10)

# Validations model
class Validations(models.Model):
    """
    Validations model
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False)
    algorithm = models.CharField(max_length = 30)
    timestamp = models.IntegerField(default=-1)
    accuracy = models.DecimalField(max_digits=20,decimal_places=10,default='-1.0000000000')
    timetotrain = models.DecimalField(max_digits=20,decimal_places=10,default='-1.0000000000')
    adaptability = models.DecimalField(max_digits=20,decimal_places=10,default='-1.0000000000')

# Portfolio model
class Portfolio(models.Model):
    """
    Portfolio model
    """
    name = models.CharField(max_length=150, unique=True)
    user = models.ForeignKey(User, related_name='portfolios', on_delete=models.CASCADE, null=False)
    items = models.ManyToManyField(Item)

    #def __unicode__(self):
    #    return '%s' % (self.owner.username)

# Token receiver
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
