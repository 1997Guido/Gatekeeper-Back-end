from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from gatekeeper.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ("pk", "first_name", "last_name", "date_of_birth", "gender", "email", "username")

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }

class RegisterSerializer(RegisterSerializer):
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


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
