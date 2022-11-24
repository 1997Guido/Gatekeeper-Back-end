from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer
from .models import Users
from django.http import HttpResponse
from .functions.RegisterLogic import RegisterLogic
from .functions.ProfileLogic import ProfileLogic
from .functions.QrCodeGenerator import QrCodeGenerator
from .functions.QrCodeScanner import QrCodeScanner

# Create your views here.

class UsersView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_def = UserSerializer

def RegisterApi(request):
    return HttpResponse(RegisterLogic())

def QrCodeGeneratorApi(request):
    return HttpResponse(QrCodeGenerator())

def QrCodeScannerApi(request):
    return HttpResponse(QrCodeScanner)

def ProfileApi(request):
    return HttpResponse(ProfileLogic())