from rest_framework import serializers
from .models import UserProfile


#this code serializes our model so it can be show in a readable format. you can configure which fields to serialize

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'age', 'gender', 'email', 'username')

