from ..models import UserProfile
import requests

def ProfileLogic(request):
    user=UserProfile.objects.filter(user=request.user)
    return (user)
