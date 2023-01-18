from ..models import UserProfile
from ..models import Event
import json

# Logic for viewing a single event

def SingleEventView(request):
    pkdata= json.loads(request.body)
    event = (
        Event.objects.filter(pk=pkdata["pk"])
        .values(
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
            "EventIsFree",
            "EventPrice",
            "EventMaxGuests",
            "EventCurrentGuests",
            "EventMinimumAge",
            "EventOrganizer",
            "EventOwner",
        )
        .first()
    )
    return(event)