import contextlib
import json
import re

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags

from apps.developer.models import Bot, WebHook
from apps.notification.utilities import notify
from apps.vit.models import Comment, Embed, Plustag, Vit

from .tasks import send_vit_mention_email, send_vit_webhook_request


def find_vit_mention(vit: Vit):
    """
    Find the Mention in the Vit Create a notification also send an email to the mentioned user
    Prams: vit
    """
    results = re.findall("(^|[^@\w])@(\w{1,150})", vit.body)
    for result in results:
        result = result[1]
        if (
            User.objects.filter(username=result).exists()
            and result != vit.user.username
        ):
            vit.mentions.add(User.objects.get(username=result))
            notify(
                message=f"""{vit.user.username.title()} Mentioned You in a Vit""",
                notification_type="mention",
                to_user=User.objects.get(username=result),
                by_user=vit.user,
                link=reverse_lazy("vit_detail", kwargs={"pk": vit.pk}),
            )

            if Bot.objects.filter(user=User.objects.get(username=result)).exists():
                bot = Bot.objects.get(user=User.objects.get(username=result))
                send_vit_webhook_request(bot.id, vit.id)

            if User.objects.get(username=result).profile.email_notif:
                send_vit_mention_email(vit.id, result)


def find_plustags(vit: Vit):
    for word in vit.body.split():
        if word[0] == "+" and word[1] != " ":
            plustag = Plustag.objects.get_or_create(name=word[1:].lower())
            vit.plustag.add(plustag[0])


def paginator_limit(request):
    """
    Paginator limit
    """
    limit = request.GET.get("limit", 10)
    return 10 if limit == "0" else limit
