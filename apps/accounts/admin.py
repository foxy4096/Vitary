from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.TabularInline):
    model = Profile
    fields = ['image', 'email_notif']
    readonly_fields = ['follows']
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
