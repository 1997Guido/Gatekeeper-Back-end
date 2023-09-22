from django.contrib import admin
from gatekeeper.api.models import Event, Image


# Copyright © 2023, Mike Vermeer & Guido Erdtsieck, All rights reserved.

admin.site.register(Event)
admin.site.register(Image)