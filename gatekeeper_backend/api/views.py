from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import UserProfileSerializer
from .serializers import EventSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.http import HttpRequest
from .functions.ProfileLogic import ProfileLogic
from .functions.QrInfoLogic import QrInfoLogic
from .functions.QrDecryptionLogic import QrDecryptionLogic
from .functions.QrCodeScanner import QrCodeScanner
from .functions.AuthCheck import AuthCheck
from .functions.EventCreation import EventCreation
from .functions.SingleEventView import SingleEventView
from django.http import JsonResponse
from .models import UserProfile
from .models import Event
from rest_framework.views import APIView
# These are views(functions) which are ran when the frontend calls their specified paths(in urls.py)


def QrCodeGeneratorApi(request):
    return HttpResponse(QrInfoLogic(request))

def QrCodeVerificatorApi(request):
    return HttpResponse(QrDecryptionLogic(request))

def QrCodeScannerApi(request):
    return HttpResponse(QrCodeScanner())

def AuthCheckApi(request):
    return HttpResponse(AuthCheck(request))

def ProfileApi(request):
    return JsonResponse(ProfileLogic(request),safe=False)

def SingleEventApi(request):
    return JsonResponse(SingleEventView(request),safe=False)

class EventCreationApi(generics.CreateAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer

class EventViewApi(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer
    queryset = Event.objects.all()

class UserProfileView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    serializer_def = UserProfileSerializer
    queryset = UserProfile.objects.all()