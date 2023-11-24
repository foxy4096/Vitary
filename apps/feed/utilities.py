import re
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from apps.notification.utilities import notify
from apps.feed.models import Feed

from .tasks import send_feed_mention_email


def find_feed_mention(feed):
    """
    Find the Mention in the feed Create a notification also send an email to the mentioned user
    Prams: feed
    """
    results = re.findall("(^|[^@\w])@(\w{1,150})", feed.body)
    for result in results:
        result = result[1]
        if (
            User.objects.filter(username=result).exists()
            and result != feed.user.username
        ):
            feed.mentions.add(User.objects.get(username=result))
            notify(
                message=f"""{feed.user.username.title()} Mentioned You in a feed""",
                notification_type="mention",
                to_user=User.objects.get(username=result),
                by_user=feed.user,
                link=reverse_lazy("feed_detail", kwargs={"pk": feed.pk}),
            )

            if User.objects.get(username=result).userprofile.email_notif:
                send_feed_mention_email(feed.id, result)
