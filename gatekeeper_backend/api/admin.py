from django.contrib import admin
from .models import UserProfile
from .models import QrCode

class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Register your models here.
admin.site.register(QrCode)
admin.site.register(UserProfile, UserProfileAdmin)
