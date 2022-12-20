from ..models import UserProfile
from ..models import Event
import json

def EventCreation(request):
    jsonData = json.loads(request.body)
    Event.objects.create(
            EventOwner_id=request.user.pk,
            EventTitle=jsonData["EventTitle"],
        )
    return("Event Created")