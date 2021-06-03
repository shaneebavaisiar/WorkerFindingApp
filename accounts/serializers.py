from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=50)
    password=serializers.CharField(max_length=50)