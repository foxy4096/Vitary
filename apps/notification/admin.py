from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Register the `Notification` model with the admin site.

    Args:
        admin.ModelAdmin: The admin model class.

    Attributes:
        autocomplete_fields (list): The list of fields to enable autocomplete for.
    """

    autocomplete_fields = ["sender", "receiver"]
