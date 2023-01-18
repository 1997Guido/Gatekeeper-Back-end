from django.db import models
from django.contrib.auth.models import AbstractUser

#This is the model for our Database Images.
#This is a custom user model which inherits most of its fields from the default UserModel created by Django.
#Importing and using the AbstractUser 'functions' make this possible.
#By using the default user model, u can use the built in authentication features(login etc..).
#The code below are the 'custom' fields i added to the default user model.
#Like age,gender and QrUid. the QrUid is the field for the unique id generated for each user in QrCodeGenerator.py

class UserProfile(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True, )
    GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Undefined', 'Undefined'),
    )
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default=False, null=False)
    QrUid = models.CharField(max_length=8, null=False, default=0)
    profilepicture = models.ImageField(upload_to='profile_images', null=True, blank=True)

#This is the model for our Events.
#The EventInvitedGuests field is a many to many field which allows a user to invite other users to an event.

class Event(models.Model):
    EventOwner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    EventTitle = models.CharField(max_length=12, null=False)
    EventDate = models.DateField(null=False)
    EventTimeStart = models.TimeField(null=False)
    EventTimeEnd = models.TimeField(null=False)
    EventLocation = models.CharField(max_length=50, null=False)
    EventDescription = models.CharField(max_length=100, null=False)
    EventInvitedGuests = models.ManyToManyField(UserProfile, related_name='EventGuests', blank=True)
    EventIsPrivate = models.BooleanField(default=False)
    EventIsCancelled = models.BooleanField(default=False)
    EventIsFree = models.BooleanField(default=False)
    EventPrice = models.DecimalField(max_digits=5, decimal_places=2,default=0, blank=True)
    EventMaxGuests = models.IntegerField(null=False, default=50)
    EventCurrentGuests = models.IntegerField(null=False, default=0)
    EventMinimumAge = models.IntegerField(null=False, default=0)
    EventOrganizer = models.CharField(max_length=50)
    def __str__(self):
        return self.EventTitle

#This is the model for our Images.
#The Image field is a ImageField which allows us to upload images to our database.
#The LinkedToEvent field is a foreign key which allows us to link an image to an event.

class Image(models.Model):
    Image = models.ImageField(upload_to='images', null=False, blank=False)
    Title = models.CharField(max_length=50, null=False, default='Image')
    Description = models.CharField(max_length=100, null=True)
    Owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.Title

