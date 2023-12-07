from allauth.account.adapter import DefaultAccountAdapter
from api.models import Event, Image, User
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

# this code serializes our model so it can be show in a readable format. you can configure which fields to serialize
# and how they are serialized


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    date_of_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES)

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "date_of_birth": self.validated_data.get("date_of_birth", ""),
            "gender": self.validated_data.get("gender", ""),
        }


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)

        user.first_name = form.cleaned_data.get("first_name")
        user.last_name = form.cleaned_data.get("last_name")
        user.date_of_birth = form.cleaned_data.get("date_of_birth")
        user.gender = form.cleaned_data.get("gender")

        if commit:
            user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    profilepicture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "pk",
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "email",
            "username",
            "ProfilePicture",
            "profilepicture_url",
        )

    def get_profilepicture_url(self, obj):
        if obj.ProfilePicture:
            return obj.ProfilePicture.Image.url
        else:
            return None


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("Image", "Title", "Description", "Owner", "id")


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "pk",
            "EventTitle",
            "EventDate",
            "EventTimeStart",
            "EventTimeEnd",
            "EventLocation",
            "EventDescription",
            "EventInvitedGuests",
            "EventIsPrivate",
            "EventIsCancelled",
            "EventMaxGuests",
            "EventMinimumAge",
            "EventOrganizer",
            "EventOwner",
            "EventCurrentGuests",
            "EventPrice",
            "EventIsFree",
            "EventBanner",
        )
