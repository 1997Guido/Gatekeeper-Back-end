from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Image
from .models import UserProfile
from .models import Event
#With list_display u can configure which fields should be shown when looking at a list of records in the User table
#This class edits the admin panel so it also shows our custom fields. this happens at 'fields'


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'id')
    readonly_fields = ('id',)
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional Info',
            {
                'fields':(
                    'date_of_birth',
                    'gender',
                    'QrUid',
                    'Images',
                )
            }
        )
    )
admin.site.register(Event)
admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(Image)
