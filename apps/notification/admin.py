from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'date', 'is_read',
                    'notification_type', 'to_user', 'by_user')
    list_filter = ('is_read', 'notification_type')


admin.site.register(Notification, NotificationAdmin)
