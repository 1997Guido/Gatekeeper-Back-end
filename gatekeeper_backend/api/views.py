from rest_framework import generics
from rest_framework import viewsets
from .serializers import UserProfileSerializer
from .serializers import UserNameSerializer
from .serializers import EventSerializer
from .serializers import ImageSerializer
from rest_framework import status
from django.http import HttpResponse
from .functions.QrCodeVerificator import QrCodeVerificator
from .functions.AuthCheck import AuthCheck
from django.http import JsonResponse
from rest_framework.response import Response
from .models import UserProfile
from .functions.QrCodeGenerator import QrCodeGenerator
from .models import Event
from .models import Image
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import json
from rest_framework import permissions


# These are views(functions) which are ran when the frontend calls their specified paths(in urls.py)
# They are called by the frontend using the axios library



def QrCodeGeneratorApi(request):
    return HttpResponse(QrCodeGenerator(request))

def QrCodeVerificatorApi(request):
    return HttpResponse(QrCodeVerificator(request))

def AuthCheckApi(request):
    return HttpResponse(AuthCheck(request))

def EventEditApi(request):
    data = json.loads(request.body)
    event = Event.objects.get(pk=data["pk"])
    serializer = EventSerializer(event, data)
    if request.user.pk == event.EventOwner.pk:
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Event edited")
        else:
            return JsonResponse(serializer.errors)
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
    def get_queryset(self):
        if self.request.query_params.get('allusers') == 'yes':
            return (UserProfile.objects.all())
        if self.request.query_params.get('allusers') == 'me':
            return UserProfile.objects.filter(pk=self.request.user.pk)
        if self.request.query_params.get('allusers') == 'picture':
            user = UserProfile.objects.get(pk=self.request.user.pk)
            return Image.objects.filter(pk=user.ProfilePicture)



class EventViewApiPersonal(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer
    def get_queryset(self):
        return Event.objects.filter(EventOwner=self.request.user.pk)



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
        if self.request.query_params.get('allusers') == 'me':
            return UserProfile.objects.filter(pk=self.request.user.pk)




class ProfileEditApi(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    serializer_def = UserProfileSerializer
    def get_object(self):
        return UserProfile.objects.get(pk=self.request.user.pk)

class ProfileDeleteApi(generics.DestroyAPIView):
    serializer_class = UserProfileSerializer
    serializer_def = UserProfileSerializer
    def get_object(self):
        return UserProfile.objects.get(pk=self.request.user.pk)

def SetProfileImage(request):
    data = json.loads(request.body)
    user = UserProfile.objects.get(pk=request.user.pk)
    image = Image.objects.get(pk=data["pictureid"])
    user.ProfilePicture = image
    user.save()
    return HttpResponse("Profile image set")



class ImageViewApi(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        if self.request.query_params.get('allmypictures') == 'yes':
            Images = Image.objects.filter(Owner=self.request.user.pk)
            serializer = ImageSerializer(Images, many=True)
            return Response(serializer.data)
        if self.request.query_params.get('allmypictures') == 'profilepicture':
            user = UserProfile.objects.get(pk=self.request.user.pk)
            serializer = ImageSerializer(user.ProfilePicture)
            return JsonResponse(serializer.data)

    def post(self, request):
        Images_serializer = ImageSerializer(data=request.data)
        if Images_serializer.is_valid():
            Images_serializer.save()
            Images_serializer.save(Owner=self.request.user)
            user = UserProfile.objects.get(pk=self.request.user.pk)
            user.Images.set = Image.objects.filter(Owner=self.request.user.pk)
            user.save()
            return JsonResponse(Images_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', Images_serializer.errors)
            return JsonResponse(Images_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        imagepk = self.request.query_params.get('pk')
        image = Image.objects.get(pk=imagepk)
        if image.Owner.pk == request.user.pk:
            image.delete()
            return HttpResponse("Image deleted")
        else:
            return HttpResponse("You are not the owner of this image")
