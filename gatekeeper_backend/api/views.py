import json
import stat

from django.http import HttpResponse, JsonResponse
from requests import delete
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.functions.AuthCheck import AuthCheck
from api.functions.QrCodeGenerator import QrCodeGenerator
from api.functions.QrCodeGenerator import QrCodeGenerator
from api.functions.QrCodeVerificator import QrCodeVerificator
from api.models import Event, Image, User
from api.serializers import (EventSerializer, ImageSerializer, UserNameSerializer,
                          UserSerializer)
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
# This view runs the QrCodeGenerator function and returns the encrypted qr code to the frontend
def QrCodeGeneratorApi(request):
    return HttpResponse(QrCodeGenerator(request))


# This views runs the QrCodeVerificator function and returns the user data to the frontend
def QrCodeVerificatorApi(request):
    return HttpResponse(QrCodeVerificator(request))


# This view runs the AuthCheck function and returns a true if the user is authenticated and a false if the user is not authenticated
def AuthCheckApi(request):
    return HttpResponse(AuthCheck(request))



class EventCreateView(generics.CreateAPIView):
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['EventOwner'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        param = self.request.query_params.get("show", None)

        if param:
            match param:
                case "all":
                    pass
                case "invited":
                    queryset = queryset.filter(EventInvitedGuests__pk=self.request.user.pk)
                case "single":
                    pk = self.kwargs.get("pk", None)
                    if pk is not None:
                        queryset = queryset.filter(pk=pk)
                case "owned":
                    queryset = queryset.filter(EventOwner=self.request.user.pk)

        return queryset

class EventDelete(generics.DestroyAPIView):
    serializer_class = EventSerializer

    def get_object(self):
        obj = Event.objects.get(pk=self.kwargs['pk'])
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.EventOwner == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You are not the owner of this event"}, status=status.HTTP_403_FORBIDDEN)



class EventEdit(generics.UpdateAPIView):
    serializer_class = EventSerializer

    def get_object(self):
        obj = Event.objects.get(pk=self.kwargs['pk'])
        return obj

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            if instance.EventOwner == request.user:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"error": "You are not the owner of this event"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





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
    
class EventDelete(APIView):

    def delete(self, request):
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
                user = User.objects.get(username=value["label"])
                event.EventInvitedGuests.remove(user.pk)
            return HttpResponse("Users uninvited")
        if data["inv"] == "Invite":
            for value in data["invitedUsers"]:
                user = User.objects.get(username=value["label"])
                event.EventInvitedGuests.add(user.pk)
            return HttpResponse("Users invited")
    else:
        return HttpResponse("You are not the owner of this event")


# This is a class based view that handles Event creation
# it is a subclass to the APIView class
# the APIView class is a builtin class from the rest_framework library


# This is a class based view that handles Profile viewing
# If allusers is set to yes, it returns all users in the database
# If allusers is set to me, it returns the user that is logged in
# If allusers is set to picture, it returns the profilepicture(pk) of the user that is logged in
class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    serializer_def = UserSerializer

    def get_queryset(self):
        if self.request.query_params.get("allusers") == "yes":
            return User.objects.all()
        if self.request.query_params.get("allusers") == "me":
            return User.objects.filter(pk=self.request.user.pk)
        if self.request.query_params.get("allusers") == "picture":
            user = User.objects.get(pk=self.request.user.pk)
            return Image.objects.filter(pk=user.ProfilePicture)


# This is a class based view that returns all events the logged in user is owner of
class EventViewApiPersonal(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(EventOwner=self.request.user.pk)


# this is a class based view that returns the event with the specified pk
class ViewSingleEvent(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer

    def get_queryset(self):
        event = Event.objects.filter(pk=self.request.query_params.get("pk"))
        return event


# this is a class based view that returns a list of all users invited to the event that is specified by the pk
def getInvitedUsers(request):
    data = json.loads(request.body)
    event = Event.objects.get(pk=data["pk"])
    return JsonResponse(list(event.EventInvitedGuests.values()), safe=False)


#
class UsernameViewApi(generics.ListAPIView):
    serializer_class = UserNameSerializer
    serializer_def = UserNameSerializer

    def get_queryset(self):
        if self.request.query_params.get("allusers") == "yes":
            return User.objects.all()
        if self.request.query_params.get("allusers") == "me":
            return User.objects.filter(pk=self.request.user.pk)


class ProfileEditApi(generics.UpdateAPIView):
    serializer_class = UserSerializer
    serializer_def = UserSerializer

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)


class ProfileDeleteApi(generics.DestroyAPIView):
    serializer_class = UserSerializer
    serializer_def = UserSerializer

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)


def SetProfileImage(request):
    data = json.loads(request.body)
    user = User.objects.get(pk=request.user.pk)
    image = Image.objects.get(pk=data["pictureid"])
    user.ProfilePicture = image
    user.save()
    return HttpResponse("Profile image set")


class ImageViewApi(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        if self.request.query_params.get("allmypictures") == "yes":
            Images = Image.objects.filter(Owner=self.request.user.pk)
            serializer = ImageSerializer(Images, many=True)
            return Response(serializer.data)
        if self.request.query_params.get("allmypictures") == "profilepicture":
            user = User.objects.get(pk=self.request.user.pk)
            if user.ProfilePicture == None:
                return HttpResponse("No profile picture")
            else:
                serializer = ImageSerializer(user.ProfilePicture)
            return JsonResponse(serializer.data)

    def post(self, request):
        Images_serializer = ImageSerializer(data=request.data)
        if Images_serializer.is_valid():
            Images_serializer.save()
            Images_serializer.save(Owner=self.request.user)
            user = User.objects.get(pk=self.request.user.pk)
            user.Images.set = Image.objects.filter(Owner=self.request.user.pk)
            user.save()
            return JsonResponse(Images_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("error", Images_serializer.errors)
            return JsonResponse(
                Images_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        imagepk = self.request.query_params.get("pk")
        image = Image.objects.get(pk=imagepk)
        if image.Owner.pk == request.user.pk:
            image.delete()
            return HttpResponse("Image deleted")
        else:
            return HttpResponse("You are not the owner of this image")
