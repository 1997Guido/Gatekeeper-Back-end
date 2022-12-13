from rest_framework import serializers
from .models import UserProfile
from dj_rest_auth.registration.serializers import RegisterSerializer


#this code serializes our model so it can be show in a readable format. you can configure which fields to serialize

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
        fields = ('first_name', 'last_name', 'age', 'gender', 'email', 'username')

