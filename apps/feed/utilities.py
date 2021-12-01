import re
import datetime

from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from apps.notification.utilities import notify


def find_mention(**kwargs):
    """
    Find the Mention in the Feed or Feed's Comment and then Create A Notification
    Prams: request, body, ntype=> In uppercase => [FEED, COMMENT] and Feed or Feed Object and Comment Object
    If FEED => Also give the feed object
    If COMMENT => Give the feed object and comment object
    """
    results = re.findall("(^|[^@\w])@(\w{1,150})", kwargs['body'])
    for result in results:
        result = result[1]
        if User.objects.filter(username=result).exists() and result != kwargs['request'].user.username:
            if kwargs['ntype'].upper() == "FEED":
                notify(message=f"{kwargs['request'].user.username.title()} Mentioned You in a Feed - '{kwargs['feed'].body}'", notification_type="mention",
                       to_user=User.objects.get(username=result).profile, by_user=kwargs['request'].user.profile, link=reverse_lazy('feed_detail', kwargs={'pk': kwargs['feed'].pk}))
                if kwargs['feed'].created_on <= timezone.now() + datetime.timedelta(days=10) and User.objects.get(username=result).profile.email_notif:
                    send_mail(
                        subject=f"{kwargs['request'].user.username.title()} mentioned you in a Feed.",
                        message=f"""
                    {kwargs['request'].user.username.title()} wrote \n
                    {kwargs['body']}\n
                    You are reciving this email because you have Send Email Notification turned on on our site.""",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[
                            User.objects.get(username=result).email],
                    )
            elif kwargs['ntype'].upper() == "COMMENT":
                comment_id = kwargs['comment'].pk
                notify(message=f"{kwargs['request'].user.username.title()} Mentioned You in a Feed's Comment - {kwargs['comment'].body}", notification_type="mention",
                       to_user=User.objects.get(username=result).profile, by_user=kwargs['request'].user.profile, link=reverse_lazy('feed_detail', kwargs={'pk': kwargs['feed'].pk}) + f'#comment-{comment_id}')
                if kwargs['comment'].created_on <= timezone.now() + datetime.timedelta(days=10) and User.objects.get(username=result).profile.email_notif:
                    send_mail(
                        subject=f"{kwargs['request'].user.username.title()} mentioned you in a comment.",
                        message=f"""
                    {kwargs['request'].user.username.title()} wrote \n
                    {kwargs['body']}\n
                    You are reciving this email because you have Send Email Notification turned on on our site.""",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[User.objects.get(username=result).email],
                    )
