from xmlrpc.client import ServerProxy
from colorama import Style
from rest_framework import serializers
from .models import Ticket
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
    print('---: ' + username)
    print('---: ' + password)

    if username and password:
      user = authenticate(
        request  = self.context.get('request'),
        username = username,
        password = password
      )

      if user is None or not user.is_active:
        raise serializers.ValidationError('[Error]Login Failed')
      data['user'] = user

      return data