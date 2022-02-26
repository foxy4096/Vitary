from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from apps.develop.models import DevProfile
from .models import Profile, Group, GroupInvitation


class ProfileInline(admin.StackedInline):
    """
    Including the profile model in the user model by inline admin
    """
    model = Profile
    readonly_fields = ['profile_image', 'follower_count', 'following_count']
    fields = ['profile_image', 'image', 'email_notif', 'verified', 'bio', 'follower_count', 'following_count', 'header_image', 'badges']
    can_delete = False

class DevProfileInline(admin.StackedInline):
    """
    Include the dev profile in the user model by inline admin
    """
    model = DevProfile

def make_verified(self, request, queryset):
    """
    Make Selected users profile verified
    """
    for user in queryset:
        user.profile.verified = True
        user.profile.save()
    self.message_user(request, "Selected users verified")
make_verified.short_description = "Make Selected Users Verified"

def make_unverified(self, request, queryset):
    """  
    Make Selected users profile unverified
    """
    for user in queryset:
        user.profile.verified = False
        user.profile.save()
    self.message_user(request, "Selected users unverified")
make_unverified.short_description = "Make Selected Users Unverified"



class UserAdmin(BaseUserAdmin):
    """
    Adding the profile inline in user model admin
    """
    inlines = [ProfileInline, DevProfileInline]
    actions = [make_verified, make_unverified]

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_public']
    list_filter = ['is_public']
    search_fields = ['name']
    ordering = ['name']
    list_editable = ['is_public']


class GroupInvitationAdmin(admin.ModelAdmin):
    list_display = ['group', 'user', 'invited_by', 'date', 'is_accepted']
    list_filter = ['group', 'user', 'invited_by', 'date', 'is_accepted']
    search_fields = ['group', 'user', 'invited_by', 'date', 'is_accepted']
    ordering = ['group', 'user', 'invited_by', 'date', 'is_accepted']
    list_editable = ['is_accepted']




# Registering the model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Group, GroupAdmin)
admin.site.register(GroupInvitation, GroupInvitationAdmin)