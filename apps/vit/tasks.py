import contextlib
import json
import re
import validators
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags

# import dramatiq
from apps.developer.models import Bot

from apps.vit.models import Embed, Vit


# @dramatiq.actor(max_retries=3, queue_name="vit")
def send_vit_mention_email(vit_id, mention):
    """
    Send an email to the user who was mentioned in the vit.
    """
    vit = Vit.objects.get(pk=vit_id)
    subject = f"{vit.user.username or vit.user.get_full_name()} mentioned you in a Vit."
    html_message = render_to_string(
        "vit/email/vit_mention.html",
        {
            "from": vit.user,
            "vit": vit,
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


# @dramatiq.actor(max_retries=3, queue_name="vit")
def send_vit_webhook_request(bot_id, vit_id):
    """
    Send a webhook request to the bot.
    """
    vit = Vit.objects.get(pk=vit_id)
    bot = Bot.objects.get(pk=bot_id)
    for webhook in bot.webhook_set.filter(event_type="on_vit_mention"):
        auth_key = bot.private_key if webhook.required_authentication else ""
        try:
            requests.request(
                method=webhook.method,
                url=webhook.payload_url,
                json=vit.to_json(),
                headers={
                    "X-API-Key": auth_key,
                },
            )
        except Exception:
            print(f"""Error while sending webhook {webhook.payload_url}""")


# @dramatiq.actor(max_retries=3, queue_name="vit")
def find_embed_url(vit_id):
    """
    Find the Url in the Vit Create an embed
    Prams: vit
    """
    vit = Vit.objects.get(pk=vit_id)
    for url in vit.body.strip().replace("\n", " ").replace("\t", " ").replace("\r", " ").split(" "):
        url: str = url
        print(validators.url(url))
        if validators.url(url) and not any(
            [
                url.startswith("https://vitary.pythonanywhere.com"),
                url.startswith("vitary.pythonanywhere.com"),
                url.startswith("http://vitary.pythonanywhere.com"),
            ]
        ):
            with contextlib.suppress(Exception):
                res = requests.get(url)
                soup = BeautifulSoup(res.text, "html.parser")
                embed = Embed.objects.get_or_create(url=url, vit=vit)[0]
                embed.title = soup.title.string
                embed.description = (
                    soup.find("meta", property="og:description")["content"] or ""
                )
                embed.image_url = (
                    soup.find("meta", property="og:image")["content"] or ""
                )
                embed.save()
