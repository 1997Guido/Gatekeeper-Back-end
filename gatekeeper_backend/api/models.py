from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False, null=False, default="John")
    last_name = models.CharField(max_length=30, blank=False, null=False, default="Doe")
    date_of_birth = models.DateField(null=False, blank=False, default="1970-01-01")
    email = models.EmailField(max_length=254, blank=False, null=False)
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Undefined", "Undefined"),
    )
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default=False, null=False)
    QrUid = models.CharField(max_length=36, null=False, default=uuid4, unique=True)
    ProfilePicture = models.OneToOneField(
        "Image",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="profile_picture",
    )

    @property
    def generate_uuid_for_user(self):
        self.QrUid = uuid4()
        self.save()
        return self.QrUid


class Event(models.Model):
    EventOwner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="owned_events",
    )
    EventTitle = models.CharField(max_length=12, null=False)
    EventBanner = models.ImageField(upload_to="images", null=True, blank=True)
    EventDate = models.DateField(null=False)
    EventTimeStart = models.TimeField(null=False)
    EventTimeEnd = models.TimeField(null=False)
    EventLocation = models.CharField(max_length=50, null=False)
    EventDescription = models.CharField(max_length=100, null=False)
    EventInvitedGuests = models.ManyToManyField(User, related_name="invited_to_events", blank=True)
    EventIsPrivate = models.BooleanField(default=False)
    EventIsCancelled = models.BooleanField(default=False)
    EventIsFree = models.BooleanField(default=False)
    EventPrice = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    EventMaxGuests = models.IntegerField(null=False, default=50)
    EventCurrentGuests = models.IntegerField(null=False, default=0)
    EventMinimumAge = models.IntegerField(null=False, default=0)
    EventOrganizer = models.CharField(max_length=50)

    def is_invited(self, user):
        # Returns a boolean indicating whether a user is invited to the event
        return user in self.EventInvitedGuests.all()

    @property
    def guest_names(self):
        return self.EventInvitedGuests.all().values_list("username", flat=True)

    def __str__(self):
        return self.EventTitle


class Image(models.Model):
    Image = models.ImageField(upload_to="images", null=False, blank=False)
    Title = models.CharField(max_length=50, null=False, default="Image")
    Description = models.CharField(max_length=100, null=True)
    Owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="owned_images",
    )

    def set_owner(self, user):
        self.Owner = user
        self.save()

    def __str__(self):
        return self.Title
