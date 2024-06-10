from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(recipient, actor, verb, object_type, object_id, is_read=False):
    """
    Create a notification for a user.

    Parameters:
    - actor: The user who initiated the notification.
    - recipient: The user who will receive the notification.
    - verb: A description or action associated with the notification.
    - object_type: The type of object related to the notification.
    - object_id: The id of the object related to the notification.
    - is_read: A boolean indicating whether the notification has been read.

    Returns:
    Notification: The created notification object.
    """
    return Notification.objects.get_or_create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        object_type=object_type,
        object_id=object_id,
        is_read=is_read,
    )
