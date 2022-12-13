from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import UserProfileSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.http import HttpRequest
from .functions.ProfileLogic import ProfileLogic
from .functions.QrInfoLogic import QrInfoLogic
from .functions.QrCodeScanner import QrCodeScanner
from .functions.AuthCheck import AuthCheck
from django.http import JsonResponse
# These are views(functions) which are ran when the frontend calls their specified paths(in urls.py)

class UserProfileView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    serializer_def = UserProfileSerializer


def QrCodeGeneratorApi(request):
    return JsonResponse(QrInfoLogic(request),safe=False)

def QrCodeScannerApi(request):
    return HttpResponse(QrCodeScanner())


def AuthCheckApi(request):
    return HttpResponse(AuthCheck(request))

def ProfileApi(request):
    return JsonResponse(ProfileLogic(request),safe=False)