from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import UserProfileSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.http import HttpResponse
from .functions.RegisterLogic import RegisterLogic
from .functions.ProfileLogic import ProfileLogic
from .functions.QrCodeGenerator import QrCodeGenerator
from .functions.QrCodeScanner import QrCodeScanner

# These are views(functions) which are ran when the frontend calls their specified paths(in urls.py)

class UserProfileView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_def = UserProfileSerializer

def RegisterApi(request):
    return HttpResponse(RegisterLogic())

def QrCodeGeneratorApi(request):
    return HttpResponse(QrCodeGenerator())

def QrCodeScannerApi(request):
    return HttpResponse(QrCodeScanner)

def ProfileApi(request):
    return HttpResponse(ProfileLogic())

def Login_User(request):
    return HttpResponse()