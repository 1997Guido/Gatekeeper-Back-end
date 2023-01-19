from rest_framework import serializers
from .models import UserProfile
from .models import Event
from .models import Image
from dj_rest_auth.registration.serializers import RegisterSerializer


# this code serializes our model so it can be show in a readable format. you can configure which fields to serialize
# and how they are serialized

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    date_of_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=UserProfile.GENDER_CHOICES)
    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
            'gender': self.validated_data.get('gender', '')
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('pk', 'first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'username', 'ProfilePicture')

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('Image', 'Title', 'Description', 'Owner', 'id')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('pk','EventTitle', 'EventDate', 'EventTimeStart', 'EventTimeEnd', 'EventLocation', 'EventDescription', 'EventInvitedGuests', 'EventIsPrivate', 'EventIsCancelled','EventMaxGuests', 'EventMinimumAge', 'EventOrganizer', 'EventOwner', "EventCurrentGuests", "EventPrice", "EventIsFree")