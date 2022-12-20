from ..models import UserProfile
from ..models import Event

def EventView(request):
    eventList = list(Event.objects.all())
    return(eventList)