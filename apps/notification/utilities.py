from django.utils import timezone
from .models import Notification


def notify(message, notification_type, to_user, by_user, link, is_read_attrub=False):
    """
    Create a notification for a user.
    """
    if to_user.userprofile.email_notif:
        notification = Notification.objects.get_or_create(
            message=message,
            notification_type=notification_type,
            to_user=to_user,
            by_user=by_user,
            link=link, 
        )[0]
        notification.is_read = is_read_attrub
        notification.date = timezone.now()
        notification.save()
        return notification
    else:
        return
