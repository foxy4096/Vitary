from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.feed.models import Feed


def send_feed_mention_email(feed_id, mention):
    """
    Send an email to the user who was mentioned in the feed.
    """
    feed = Feed.objects.get(pk=feed_id)
    subject = f"{feed.user.username or feed.user.get_full_name()} mentioned you in a feed."
    html_message = render_to_string(
        "feed/email/feed_mention.html",
        {
            "from": feed.user,
            "feed": feed,
            "subject": subject,
            "web_url": settings.WEB_HOST,
        },
    )
    text_message = strip_tags(html_message)
    mail = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[User.objects.get(username=mention).email],
    )
    mail.attach_alternative(html_message, "text/html")
    mail.send()
