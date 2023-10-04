import json

from api.functions.AuthCheck import AuthCheck
from api.functions.QrCode import QRCodeHandler
from api.models import Event, Image, User
from api.serializers import EventSerializer, ImageSerializer, UserNameSerializer, UserSerializer
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView


class QrCodeView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        qr_handler = QRCodeHandler(request)
        return HttpResponse(qr_handler.generate())

    def post(self, request):
        qr_handler = QRCodeHandler(request)
        verification_result = qr_handler.verify()

        # If no verification result
        if not verification_result:
            return Response(
                {"error": "QR Code verification failed."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user, invited = verification_result

        # If user is None, it means there was an error in verification
        if user is None:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_serializer = self.serializer_class(user)
        response_data = {"userdata": user_serializer.data}

        # Check if the user is invited and return appropriate response
        if invited:
            return Response(response_data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


def AuthCheckView(request):
    return HttpResponse(AuthCheck(request))


class IsEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.EventOwner == request.user


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsImageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.Owner == request.user


class EventCreateView(generics.CreateAPIView):
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["EventOwner"] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(generics.RetrieveAPIView):
    serializer_class = EventSerializer

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        event = self.get_object()
        serializer = self.get_serializer(event)
        param = self.request.query_params.get("show", None)
        if param is not None:
            if param == "guests":
                return Response(serializer.data["EventInvitedGuests"])
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        param = self.request.query_params.get(
            "show", "all"
        )  # Show query param value defaults to "all" if not specified

        if param:
            match param:
                case "all":
                    pass
                case "invited":
                    queryset = queryset.filter(EventInvitedGuests__pk=self.request.user.pk)
                case "owned":
                    queryset = queryset.filter(EventOwner=self.request.user.pk)
                case _:
                    raise ValidationError("Invalid 'show' parameter")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return queryset


class EventDeleteView(generics.DestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsEventOwner]

    def get_object(self):
        obj = Event.objects.get(pk=self.kwargs["pk"])
        return obj

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        self.check_object_permissions(request, event)
        self.perform_destroy(event)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventUpdateView(generics.UpdateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsEventOwner]

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        self.check_object_permissions(request, event)

        serializer = self.get_serializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventInviteView(generics.UpdateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsEventOwner]

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body)
        event = self.get_object()
        self.check_object_permissions(request, event)
        for value in data["invited"]:
            user = User.objects.get(username=value["label"])
            event.EventInvitedGuests.add(user.pk)
        return HttpResponse("Users invited")


class EventUninviteView(generics.UpdateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsEventOwner]

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body)
        event = self.get_object()
        self.check_object_permissions(request, event)
        for value in data["uninvited"]:
            user = User.objects.get(username=value["label"])
            event.EventInvitedGuests.remove(user.pk)
        return HttpResponse("Users uninvited")


class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    serializer_def = UserSerializer

    def get_queryset(self):
        param = self.request.query_params.get("show", "all")
        match param:
            case "all":
                queryset = User.objects.all()
            case "single":
                pk = self.kwargs.get("pk", None)
                if pk is not None:
                    queryset = User.objects.filter(pk=pk)
            case "me":
                queryset = User.objects.filter(pk=self.request.user.pk)
            case _:
                raise ValidationError("Invalid 'show' parameter")
        return queryset


class UsernameViewApi(generics.ListAPIView):
    serializer_class = UserNameSerializer
    serializer_def = UserNameSerializer

    def get_queryset(self):
        param = self.request.query_params.get("show", "all")
        match param:
            case "all":
                queryset = User.objects.all()
            case "single":
                pk = self.kwargs.get("pk", None)
                if pk is not None:
                    queryset = User.objects.filter(pk=pk)
            case "me":
                queryset = User.objects.filter(pk=self.request.user.pk)
            case _:
                raise ValidationError("Invalid 'show' parameter")
        return queryset


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    serializer_def = UserSerializer

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    serializer_def = UserSerializer

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        self.perform_destroy(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfilePictureView(APIView):
    def get(self, request):
        user = User.objects.get(pk=self.request.user.pk)
        if user.ProfilePicture is None:
            return HttpResponse("No profile picture")
        else:
            serializer = ImageSerializer(user.ProfilePicture)
        return JsonResponse(serializer.data)

    def patch(self, request, *args, **kwargs):
        image_id = self.kwargs.get("pk", None)
        if image_id is not None:
            user = User.objects.get(pk=self.request.user.pk)
            image = Image.objects.get(pk=image_id)
            user.ProfilePicture = image
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ImageViewApi(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        param = self.request.query_params.get("show", "all")
        match param:
            case "all":
                images = Image.objects.all()
            case "single":
                pk = self.kwargs.get("pk", None)
                if pk is not None:
                    images = Image.objects.filter(pk=pk)
            case "owned":
                images = Image.objects.filter(Owner=self.request.user.pk)
            case _:
                raise ValidationError("Invalid 'show' parameter")
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.save(Owner=self.request.user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        image_id = self.kwargs.get("pk", None)
        image = Image.objects.get(pk=image_id)
        if image.Owner.pk == request.user.pk:
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
