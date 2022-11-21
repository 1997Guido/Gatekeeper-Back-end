from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer
from .models import Users

# Create your views here.

class UsersView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer