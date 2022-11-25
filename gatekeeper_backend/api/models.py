from django.db import models
import string
import random
from django import forms
from django.contrib.auth.models import AbstractUser

#This is the model for our Database
#Users is the main database the others use its primary key as foreignkey(Many to One)

class UserProfile(models.Model):
    class Meta:  
        verbose_name_plural = 'Users'
    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
    )
    emailadress = models.CharField(max_length=32, null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=False, null=False)
    first_name = models.CharField(max_length=32, null=False)
    last_name = models.CharField(max_length=64, null=False)
    age = models.IntegerField(null=False)
    date_created = models.DateField(auto_now_add=True, null=False)
    def __str__(self):
        return self.last_name


class QrCode(models.Model):
        class Meta:  
            verbose_name_plural = 'QrCodes'
        user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
        QrUid = models.CharField(max_length=8, null=False)