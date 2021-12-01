import re
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
                notify(message=f"{kwargs['request'].user.username.title()} Mentioned You in a Feed", notification_type="mention",
                       to_user=User.objects.get(username=result).profile, by_user=kwargs['request'].user.profile, link=reverse_lazy('feed_detail', kwargs={'pk': kwargs['feed'].pk}))
            elif kwargs['ntype'].upper() == "COMMENT":
                comment_id = kwargs['comment'].pk
                notify(message=f"{kwargs['request'].user.username.title()} Mentioned You in a Feed's Comment", notification_type="mention",
                       to_user=User.objects.get(username=result).profile, by_user=kwargs['request'].user.profile, link=reverse_lazy('feed_detail', kwargs={'pk': kwargs['feed'].pk}) + f'#comment-{comment_id}')
