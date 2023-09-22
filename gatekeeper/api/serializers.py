from rest_framework import serializers

from gatekeeper.api.models import Event, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("Image", "Title", "Description", "Owner", "id")


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "pk",
            "EventTitle",
            "EventDate",
            "EventTimeStart",
            "EventTimeEnd",
            "EventLocation",
            "EventDescription",
            "EventInvitedGuests",
            "EventIsPrivate",
            "EventIsCancelled",
            "EventMaxGuests",
            "EventMinimumAge",
            "EventOrganizer",
            "EventOwner",
            "EventCurrentGuests",
            "EventPrice",
            "EventIsFree",
        )
