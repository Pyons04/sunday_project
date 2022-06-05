from dataclasses import fields
from rest_framework import serializers, exceptions
from .models import Ticket, Category
from django.contrib.auth import authenticate

class TicketSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ticket
    fields = '__all__'

class LoginSerializer(serializers.Serializer):
  username = serializers.CharField(write_only=True)
  password = serializers.CharField(
    write_only=True, 
    style = {'input_type' : 'password'}
  )

  def validate(self, data):
    username = data.get('username')
    password = data.get('password')

    if username and password:
      user = authenticate(
        request  = self.context.get('request'),
        username = username,
        password = password
      )

      if user is None or not user.is_active:
        raise exceptions.AuthenticationFailed('Login Failed')
      data['user'] = user

      return data

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'