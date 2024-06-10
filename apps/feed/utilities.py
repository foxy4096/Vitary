import re
from django.contrib.auth.models import User
from apps.notification.utilities import create_notification


def find_feed_mention(feed):
    """
    Find the Mention in the feed Create a notification
    """
    results = re.findall("(^|[^@\w])@(\w{1,150})", feed.body)
    for result in results:
        result = result[1]
        if (
            User.objects.filter(username=result).exists()
            and result != feed.user.username
        ):
            feed.mentions.add(User.objects.get(username=result))
            create_notification(
                verb="mentiond",
                recipient=User.objects.get(username=result),
                actor=feed.user,
                object_type="feed",
                object_id=feed.id,
            )
