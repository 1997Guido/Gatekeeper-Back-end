from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
import PIL
from io import BytesIO
from PIL import Image
from django.core.files import File

#This is the model for our Database


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

#This is the model for our Events.
#The EventInvitedGuests field is a many to many field which allows a user to invite other users to an event.
class Event(models.Model):
    EventOwner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    EventTitle = models.CharField(max_length=50, null=False)
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
class Image(models.Model):
    Image = models.FileField()
    ImageOwner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    LinkedToEvent = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        new_image = self.compress_images(self.image)  
# Set self.image to new_image, which is a PIL Image instance
# that has already been resized
        self.image = new_image
        super().save(*args, **kwargs)
   
    def valid_extension(self,_img):
        if '.jpg' in _img:
            return "JPEG"
        elif '.jpeg' in _img:
            return "JPEG"
        elif '.png' in _img:
            return "PNG"

# This is a method that resizes an image to a given size
# It uses the Python Imaging Library (PIL)
# The image is saved to a BytesIO object, which is then saved to the
# ImageField
    def compress_images(self,image):
        im = Image.open(image)
        width, height = im.size
        im = im.resize((width-50, height-50), PIL.Image.ANTIALIAS) 
        # create a BytesIO object
        im_io = BytesIO() 
        im.save(im_io, self.valid_extension(image.name) ,optimize=True, 
        quality=70) 
        new_image = File(im_io, name=image.name)
        return new_image

