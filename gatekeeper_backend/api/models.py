from django.db import models
import string
import random
from django import forms
from django.contrib.auth.models import AbstractUser

#This is the model for our Database
#Users is the main database the others use its primary key as foreignkey(Many to One)

class UserProfile(AbstractUser):
    pass
    age = models.IntegerField(null=False, default=0)
    def __str__(self):
        return self.username