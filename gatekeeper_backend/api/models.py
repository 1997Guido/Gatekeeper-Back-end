from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


#This is the model for our Database
#This is a custom user model which inherits most of its fields from the default UserModel created by Django.
#Importing and using the AbstractUser 'functions' make this possible.
#By using the default user model, u can use the built in authentication features(login etc..).
#The code below are the 'custom' fields i added to the default user model.
#Like age,gender and QrUid. the QrUid is the field for the unique id generated for each user in QrCodeGenerator.py


class UserProfile(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Undefined', 'Undefined'),
    )
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default=False, null=False)
    QrUid = models.CharField(max_length=8,null=False, default=0)
    def __str__(self):
        return self.username