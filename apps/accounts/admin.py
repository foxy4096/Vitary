from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.TabularInline):
    """
    Including the profile model in the user model by inline admin
    """
    model = Profile
    readonly_fields = ['profile_image',]
    fields = ['profile_image', 'image', 'email_notif', 'verified', 'bio',]
    can_delete = False


class UserAdmin(BaseUserAdmin):
    """
    Adding the profile inline in user model admin"""
    inlines = [ProfileInline,]

# Registering the model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
