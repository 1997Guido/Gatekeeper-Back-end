import json

from django.http import HttpResponse, JsonResponse
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .functions.AuthCheck import AuthCheck
from .functions.QrCodeGenerator import QrCodeGenerator
from .functions.QrCodeVerificator import QrCodeVerificator
from gatekeeper.api.models import Event, Image
from gatekeeper.users.models import User
from gatekeeper.api.serializers import EventSerializer, ImageSerializer
from gatekeeper.users.api.serializers import UserSerializer, UserNameSerializer

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


class EventCreationApi(generics.CreateAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer

    def perform_create(self, serializer):
        serializer.save(EventOwner=self.request.user)


class EventViewApi(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer
    queryset = Event.objects.all()


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


class EventViewApiPersonal(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(EventOwner=self.request.user.pk)


class ViewSingleEvent(generics.ListAPIView):
    serializer_class = EventSerializer
    serializer_def = EventSerializer

    def get_queryset(self):
        event = Event.objects.filter(pk=self.request.query_params.get("pk"))
        return event


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
            return JsonResponse(Images_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        imagepk = self.request.query_params.get("pk")
        image = Image.objects.get(pk=imagepk)
        if image.Owner.pk == request.user.pk:
            image.delete()
            return HttpResponse("Image deleted")
        else:
            return HttpResponse("You are not the owner of this image")
