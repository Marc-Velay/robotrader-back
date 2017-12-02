# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.serializers import *
from api.models import Item
import datetime

# Create your views here.

class CreateView(generics.ListCreateAPIView):

    # Gives us control over our api
    queryset = Item.objects.filter(id__lte=100)
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Save the post data when creating a new Item."""
        serializer.save()

class DetailsView(generics.RetrieveUpdateDestroyAPIView):

    # Handles REST ( GET, PUT, DELETE )
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

class item_year(generics.ListCreateAPIView):

    #Fetch correct item serializer
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        This view returns all entries for the given year through the URL
        """
        item = self.kwargs['item']
        year = self.kwargs['year']
        return Item.objects.filter(
            name = item,
            timestamp__year = year
        )[:100]

class item_month(generics.ListCreateAPIView):

    #Fetch correct item serializer
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        This view returns all entries for the given month for the given item through the URL
        """
        item = self.kwargs['item']
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Item.objects.filter(
            name = item,
            timestamp__year = year,
            timestamp__month = month
        )[:100]

class item_day(generics.ListCreateAPIView):

    #Fetch correct item serializer
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        This view returns all entries for the given day through the URL
        """
        item = self.kwargs['item']
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        return Item.objects.filter(
            name = item,
            timestamp__year = year,
            timestamp__month = month,
            timestamp__day = day
        )[:100]

class item_last24(generics.ListCreateAPIView):

    #Fetch serializer
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        This view returns the last 24 hours of a given item
        """
        item = self.kwargs['item']
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        return Item.objects.filter(
            name = item,
            timestamp__gte = date_from
        )[:100]

class UserAddView(generics.CreateAPIView):

    #Fetch serializer
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'username': token.user.username, 'id': token.user_id})

class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.UpdateAPIView):
    """View to update a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDeleteView(generics.DestroyAPIView):
    """View to delete a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
