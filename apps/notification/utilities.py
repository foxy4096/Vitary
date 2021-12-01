from django.utils import timezone
from .models import Notification


def notify(message, notification_type, to_user, by_user, link):
    """
    Create a notification for a user.
    """
    notification = Notification.objects.get_or_create(
        message=message,
        notification_type=notification_type,
        to_user=to_user,
        by_user=by_user,
        link=link
    )[0]
    notification.is_read = False
    notification.date = timezone.now()
    notification.save()
    return notification
