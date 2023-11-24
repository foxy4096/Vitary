from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """
    Including the userprofile model in the user model by inline admin
    """

    model = UserProfile
    readonly_fields = [
        "follower_count",
        "following_count",
    ]
    fields = [
        "email_notif",
        "verified",
        "bio",
        "follower_count",
        "following_count",
        "use_gravatar",
        "avatar_image",
        "header_image",
        "badges",
        "date_of_birth",
    ]
    autocomplete_fields = ["badges"]
    can_delete = False


def make_verified(self, request, queryset):
    """
    Make Selected users userprofile verified
    """
    for user in queryset:
        user.userprofile.verified = True
        user.userprofile.save()
    self.message_user(request, "Selected users verified")


make_verified.short_description = "Make Selected Users Verified"


def make_unverified(self, request, queryset):
    """
    Make Selected users userprofile unverified
    """
    for user in queryset:
        user.userprofile.verified = False
        user.userprofile.save()
    self.message_user(request, "Selected users unverified")


make_unverified.short_description = "Make Selected Users Unverified"


class UserAdmin(BaseUserAdmin):
    """
    Adding the userprofile inline in user model admin
    """

    inlines = [
        UserProfileInline,
    ]
    actions = [make_verified, make_unverified]


# Registering the model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
