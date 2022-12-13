from django.db import models
import string
import random
from django import forms
from django.contrib.auth.models import AbstractUser

#This is the model for our Database
#This is a custom user model which inherits most of its fields from the default UserModel created by Django.
#Importing and using the AbstractUser 'functions' make this possible.
#By using the default user model, u can use the built in authentication features(login etc..).
#The code below are the 'custom' fields i added to the default user model.
#Like age,gender and QrUid. the QrUid is the field for the unique id generated for each user in QrCodeGenerator.py

class UserProfile(AbstractUser):
    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
    )
    age = models.PositiveIntegerField(null=False, default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=False, null=False)
    QrUid = models.CharField(max_length=8,null=False, default=0)
    def __str__(self):
        return self.username