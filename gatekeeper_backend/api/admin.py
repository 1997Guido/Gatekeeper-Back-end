from django.contrib import admin
from .models import Users
from .models import QrCode


class UsersAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Register your models here.
admin.site.register(QrCode)
admin.site.register(Users, UsersAdmin)
