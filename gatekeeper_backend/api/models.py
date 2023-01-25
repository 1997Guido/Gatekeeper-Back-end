from django.db import models
from django.contrib.auth.models import AbstractUser

#This is the model for our Database Images.
#This is a custom user model which inherits most of its fields from the default UserModel created by Django.
#Importing and using the AbstractUser 'functions' make this possible.
#By using the default user model, u can use the built in authentication features(login etc..).
#The code below are the 'custom' fields i added to the default user model.
#Like age,gender and QrUid. the QrUid is the field for the unique id generated for each user in QrCodeGenerator.py

class UserProfile(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    date_of_birth = models.DateField(null=False, blank=False, default='2000-01-01')
    email = models.EmailField(max_length=254, blank=False, null=False)
    GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Undefined', 'Undefined'),
    )
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default=False, null=False)
    QrUid = models.CharField(max_length=8, null=False, default=0)
    Images = models.ManyToManyField('Image', related_name='UserImages', blank=True)
    ProfilePicture = models.OneToOneField('Image', on_delete=models.SET_NULL, blank=True, null=True, related_name='ProfilePicture')

#This is the model for our Events.
#The EventInvitedGuests field is a many to many field which allows a user to invite other users to an event.

class Event(models.Model):
    EventOwner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    EventTitle = models.CharField(max_length=12, null=False)
    EventBanner = models.ForeignKey('Image', on_delete=models.SET_NULL, blank=True, null=True, related_name='EventBanner')
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
#The Owner field is a foreign key which allows us to link the image to a user.
#This is done so that we can display the images uploaded by a user on their profile page.
#The Title and Description fields are just for the user to add a title and description to their image.

class Image(models.Model):
    Image = models.ImageField(upload_to='images', null=False, blank=False)
    Title = models.CharField(max_length=50, null=False, default='Image')
    Description = models.CharField(max_length=100, null=True)
    Owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.Title

