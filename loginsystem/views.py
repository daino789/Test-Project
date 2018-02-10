# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

# from .models import Pet
from .serializers import SignupSerializer, LoginSerializer, LogoutSerializer


def signup_template(request):
    return HttpResponse("test signup")
    # return render(request, 'loginsystem/signup.html')

def login_template(request):
    return render(request, 'loginsystem/login.html')


class Signup(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def create(self, request):
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            username = user.username
            raw_password = user.password

            #again set password in HASH format
            user.set_password(raw_password)
            user.save()

            user = authenticate(username=username, password=raw_password)
            
            #Generate or get TOKEN for authentication.
            token, created = self.model.objects.get_or_create(user=user) 
        
            headers = { 'access_token': token.key }
            return Response({
                "status": status.HTTP_201_CREATED,
                "success" : True,
                "message" : "Successfully Created Your Account.",
                }, headers= headers )

        return Response(serializer.errors)


class Login(viewsets.ViewSet):

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    model = Token  

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        try:
            token, created = self.model.objects.get_or_create(user=user)

        except Exception as e:
            pass
          
        headers = { 'access_token' : token.key }

        return Response({
            "status": status.HTTP_200_OK,
            "message" : 'Successfully login.'
            }, headers=headers)

 
class Logout(viewsets.ViewSet):  
    permission_classes = (AllowAny,)
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        if token:
            token.delete()

        else:
          pass

        return Response({
            "status": status.HTTP_200_OK,
            "message" : 'Successfully logout.'
            })
      