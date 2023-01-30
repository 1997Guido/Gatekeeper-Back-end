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


# This view runs the QrCodeGenerator function and returns the encrypted qr code to the frontend
def QrCodeGeneratorApi(request):
    return HttpResponse(QrCodeGenerator(request))

# This views runs the QrCodeVerificator function and returns the user data to the frontend
def QrCodeVerificatorApi(request):
    return HttpResponse(QrCodeVerificator(request))

# This view runs the AuthCheck function and returns a true if the user is authenticated and a false if the user is not authenticated
def AuthCheckApi(request):
    return HttpResponse(AuthCheck(request))


# This view is for editing a Event in the database
# It is called by the frontend when the user edits an event
# The frontend sends the data to the backend using a POST request
# The data contains a PK which is the primary key of the event in the database the user wants to edit
# It checks if the user is the owner of the event
# If the user is the owner of the event, it saves the changes to the database
# If the user is not the owner of the event, it returns a message to the frontend
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


# This view is for deleting a Event in the database
# It is called by the frontend when the user deletes an event
# The frontend sends the data to the backend using a POST request
def EventDeleteApi(request):
    data = json.loads(request.body)
    event = Event.objects.get(pk=data["eventpk"])
    if request.user.pk == event.EventOwner.pk:
        event.delete()
        return HttpResponse("Event deleted")
    else:
        return HttpResponse("You are not the owner of this event")




# This view handles invites and uninvites to and event in the database
# It is called by the frontend when the user invites or uninvites a user to an event
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


# This is a class based view that handles Event creation
# it is a subclass to the APIView class
# the APIView class is a builtin class from the rest_framework library
class EventCreationApi(generics.CreateAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer
    def perform_create(self, serializer):
        serializer.save(EventOwner=self.request.user)


# This is a class based view that handles Event viewing
class EventViewApi(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer
    queryset = Event.objects.all()


# This is a class based view that handles Profile viewing
# If allusers is set to yes, it returns all users in the database
# If allusers is set to me, it returns the user that is logged in
# If allusers is set to picture, it returns the profilepicture(pk) of the user that is logged in
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


# This is a class based view that returns all events the logged in user is owner of
class EventViewApiPersonal(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer
    def get_queryset(self):
        return Event.objects.filter(EventOwner=self.request.user.pk)


#this is a class based view that returns the event with the specified pk
class ViewSingleEvent(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer
    def get_queryset(self):
        event = Event.objects.filter(pk=self.request.query_params.get('pk'))
        return (event)


# this is a class based view that returns a list of all users invited to the event that is specified by the pk
def getInvitedUsers(request):
    data = json.loads(request.body)
    event = Event.objects.get(pk=data["pk"])
    return JsonResponse(list(event.EventInvitedGuests.values()),safe=False)



#
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
