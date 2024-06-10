from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from apps.feed.models import Feed
from apps.feed.utilities import (
    find_feed_mention,
)
from apps.notification.models import Notification


@receiver(post_save, sender=Feed)
def save_feed(sender, instance, created, **kwargs):
    if created:
        find_feed_mention(instance)

@receiver(pre_delete, sender=Feed)
def delete_feed(sender, instance, **kwargs):
    # Remove the notification
    notification = Notification.objects.filter(object_id=instance.id, object_type="feed")
    notification.delete()
