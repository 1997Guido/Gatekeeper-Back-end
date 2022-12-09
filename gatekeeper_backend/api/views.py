from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import UserProfileSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.http import HttpResponse
from .functions.ProfileLogic import ProfileLogic
from .functions.QrCodeGenerator import QrCodeGenerator
from .functions.QrCodeScanner import QrCodeScanner
from django.http import JsonResponse
# These are views(functions) which are ran when the frontend calls their specified paths(in urls.py)

class UserProfileView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    serializer_def = UserProfileSerializer
    def get_queryset(self):
        user = self.request.user
        queryset = UserProfile.objects.filter(username = user)
        return queryset


def QrCodeGeneratorApi(request):
    return HttpResponse(QrCodeGenerator())

def QrCodeScannerApi(request):
    return HttpResponse(QrCodeScanner)


#This is the profile view, it returns the profile of the user who is logged in
#request.user is the user who is logged in
def ProfileApi(request):
    if (request.user.is_authenticated):
        userId = request.user
        data = {"user": request.user}
        return JsonResponse(data)
    else:
        return HttpResponse('not authenticated')