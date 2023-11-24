from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.feed.models import Feed
from apps.feed.utilities import (
    find_feed_mention,
)


@receiver(post_save, sender=Feed)
def save_feed(sender, instance, created, **kwargs):
    if created:
        find_feed_mention(instance)
