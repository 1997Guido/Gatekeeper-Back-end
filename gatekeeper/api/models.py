from django.db import models


class Event(models.Model):
    EventOwner = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True)
    EventTitle = models.CharField(max_length=12, null=False)
    EventBanner = models.ForeignKey(
        "api.Image", on_delete=models.SET_NULL, blank=True, null=True, related_name="event_banners"
    )
    EventDate = models.DateField(null=False)
    EventTimeStart = models.TimeField(null=False)
    EventTimeEnd = models.TimeField(null=False)
    EventLocation = models.CharField(max_length=50, null=False)
    EventDescription = models.CharField(max_length=100, null=False)
    EventInvitedGuests = models.ManyToManyField("users.User", related_name="invited_to_events")
    EventIsPrivate = models.BooleanField(default=False)
    EventIsCancelled = models.BooleanField(default=False)
    EventIsFree = models.BooleanField(default=False)
    EventPrice = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    EventMaxGuests = models.IntegerField(null=False, default=50)
    EventCurrentGuests = models.IntegerField(null=False, default=0)
    EventMinimumAge = models.IntegerField(null=False, default=0)
    EventOrganizer = models.CharField(max_length=50)


    @property
    def invited_guests(self):
        return self.EventInvitedGuests.all()

    def __str__(self):
        return self.EventTitle


class Image(models.Model):
    Image = models.ImageField(upload_to="images", null=False, blank=False)
    Title = models.CharField(max_length=50, null=False, default="Image")
    Description = models.CharField(max_length=100, null=True)
    Owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, blank=True, null=True, related_name="owned_images"
    )

    def __str__(self):
        return self.Title
