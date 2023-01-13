from rest_framework import generics
from rest_framework import viewsets
from .serializers import UserProfileSerializer
from .serializers import UserNameSerializer
from .serializers import EventSerializer
from django.http import HttpResponse
from .functions.ProfileLogic import ProfileLogic
from .functions.QrInfoLogic import QrInfoLogic
from .functions.QrCodeScanner import QrCodeScanner
from .functions.QrCodeVerificator import QrCodeVerificator
from .functions.AuthCheck import AuthCheck
from django.http import JsonResponse
from .models import UserProfile
from .models import Event
# These are views(functions) which are ran when the frontend calls their specified paths(in urls.py)
import json

def QrCodeGeneratorApi(request):
    return HttpResponse(QrInfoLogic(request))

def QrCodeVerificatorApi(request):
    return HttpResponse(QrCodeVerificator(request))

def QrCodeScannerApi(request):
    return HttpResponse(QrCodeScanner())

def AuthCheckApi(request):
    return HttpResponse(AuthCheck(request))

def ProfileApi(request):
    return JsonResponse(ProfileLogic(request),safe=False)

def EventEditApi(request):
    data = json.loads(request.body)
    event = Event.objects.get(pk=data["pk"])
    serializer = EventSerializer(event, data)
    if request.user.pk == event.EventOwner.pk:
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Event edited")
        else:
            return HttpResponse('error', serializer.errors)
    else:
        return HttpResponse("You are not the owner of this event")

def EventDeleteApi(request):
    data = json.loads(request.body)
    event = Event.objects.get(pk=data["eventpk"])
    if request.user.pk == event.EventOwner.pk:
        event.delete()
        return HttpResponse("Event deleted")
    else:
        return HttpResponse("You are not the owner of this event")
    
def EventInviteApi(request):
    data = json.loads(request.body)
    event = Event.objects.get(pk=data["pk"])
    if request.user.pk == event.EventOwner.pk:
        if data["inv"] == "Uninvite":
            for value in data["invitedUsers"]:
                user = UserProfile.objects.get(username=value['label'])
                event.EventInvitedGuests.remove(user.pk)
            return HttpResponse("Users uninvited")
        if data["inv"] == "Invite":
            for value in data["invitedUsers"]:
                user = UserProfile.objects.get(username=value['label'])
                event.EventInvitedGuests.add(user.pk)
            return HttpResponse("Users invited")
    else:
        return HttpResponse("You are not the owner of this event")



class EventCreationApi(generics.CreateAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer
    def perform_create(self, serializer):
        serializer.save(EventOwner=self.request.user)

class EventViewApi(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer
    queryset = Event.objects.all()

class UserProfileView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    serializer_def = UserProfileSerializer
    queryset = UserProfile.objects.all()

class EventViewApiPersonal(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer
    def get_queryset(self):
        return Event.objects.filter(EventOwner=self.request.user.pk)

class UsernameViewApi(generics.ListAPIView):
    serializer_class = UserNameSerializer
    serializer_def = UserNameSerializer
    def get_queryset(self):
        if self.request.query_params.get('allusers') == 'yes':
            return UserProfile.objects.all()

class ViewSingleEvent(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer
    def get_queryset(self):
        event = Event.objects.filter(pk=self.request.query_params.get('pk'))
        return (event)

def getInvitedUsers(request):
    data = json.loads(request.body)
    event = Event.objects.get(pk=data["pk"])
    return JsonResponse(list(event.EventInvitedGuests.values()),safe=False)

class UsernameViewApi(generics.ListAPIView):
    serializer_class = UserNameSerializer
    serializer_def = UserNameSerializer
    def get_queryset(self):
        if self.request.query_params.get('allusers') == 'yes':
            return UserProfile.objects.all()