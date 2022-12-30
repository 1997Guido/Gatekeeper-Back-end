import json





def EventEditApi(request):
    data = json.loads(request.body)
    event = Event.objects.get(pk=data["pk"])
    serializer = EventSerializer(event, data)
    if request.user.pk == event.EventOwner.pk:
        if serializer.is_valid():
            serializer.save()
        return ("Event edited")
    else:
        return ("You are not the owner of this event")