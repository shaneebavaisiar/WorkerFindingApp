from django.shortcuts import render
from rest_framework.response import Response

from .serializers import UserRegSerializer,LoginSerializer
from rest_framework import generics
from rest_framework import mixins
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class Registration(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    def get(self,request,*args,**kwargs):
        return self.list(request, *args, **kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request, *args, **kwargs)

class UserLogin(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data.get("username")
            password=serializer.validated_data.get('password')
            user=User.objects.get(username=username)
            if(user.username==username)&(user.password==password):
                login(request,user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=204)
            return Response('failed')

class AdminLogin(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data.get("username")
            password=serializer.validated_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=204)
            return Response('failed')

class UserLogout(APIView):
    def get(self,request):
        logout(request)
        request.user.auth_token.delete()
