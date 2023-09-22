from django.db import models


class Event(models.Model):
    EventOwner = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True)
    EventTitle = models.CharField(max_length=12, null=False)
    EventBanner = models.ForeignKey(
        "api.Image", on_delete=models.SET_NULL, blank=True, null=True, related_name="event_banner"
    )
    EventDate = models.DateField(null=False)
    EventTimeStart = models.TimeField(null=False)
    EventTimeEnd = models.TimeField(null=False)
    EventLocation = models.CharField(max_length=50, null=False)
    EventDescription = models.CharField(max_length=100, null=False)
    EventInvitedGuests = models.ManyToManyField("users.User", related_name="event_guests", blank=True)
    EventIsPrivate = models.BooleanField(default=False)
    EventIsCancelled = models.BooleanField(default=False)
    EventIsFree = models.BooleanField(default=False)
    EventPrice = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    EventMaxGuests = models.IntegerField(null=False, default=50)
    EventCurrentGuests = models.IntegerField(null=False, default=0)
    EventMinimumAge = models.IntegerField(null=False, default=0)
    EventOrganizer = models.CharField(max_length=50)

    def __str__(self):
        return self.EventTitle


class Image(models.Model):
    Image = models.ImageField(upload_to="images", null=False, blank=False)
    Title = models.CharField(max_length=50, null=False, default="Image")
    Description = models.CharField(max_length=100, null=True)
    Owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, blank=True, null=True, related_name="image_owner"
    )

    def __str__(self):
        return self.Title
