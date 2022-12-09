from ..models import UserProfile
import requests
from django.http import JsonResponse
from ..models import UserProfile
from ..serializers import UserProfileSerializer


def ProfileLogic(userId):
    user = UserProfile.objects.get(pk=userId)
    return (user)
