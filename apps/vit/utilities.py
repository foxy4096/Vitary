import re
import json
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


client = requests.Session()


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
                for webhook in bot.webhook_set.all():
                    auth_key = (
                        bot.private_key if webhook.required_authentication else ""
                    )
                    print(webhook.event_type)
                    if webhook.event_type == "on_vit_mention":
                        print(f"Sending Webhook to {webhook.payload_url}")
                        try:
                            client.request(
                                method=webhook.method,
                                url=webhook.payload_url,
                                data=json.dumps(vit.to_json()),
                                headers={
                                    "Content-Type": "application/json",
                                    "X-API-Key": auth_key,
                                },
                            )
                        except:
                            print(f"""Error while sending webhook {webhook.payload_url}""")

            if User.objects.get(username=result).profile.email_notif:
                subject = f"{vit.user.username.title()} mentioned you in a Vit."
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
                    to=[User.objects.get(username=result).email],
                )
                mail.attach_alternative(html_message, "text/html")
                mail.send()


def find_comment_mention(comment: Comment):
    """
    Find the Mention in the Comment Create a notification also send an email to the mentioned user
    Prams: comment
    """
    results = re.findall("(^|[^@\w])@(\w{1,150})", comment.body)
    for result in results:
        result = result[1]
        if (
            User.objects.filter(username=result).exists()
            and result != comment.user.username
        ):
            notify(
                message=f"""{comment.user.username.title()} Mentioned You in a Comment""",
                notification_type="mention",
                to_user=User.objects.get(username=result),
                by_user=comment.user,
                link=reverse_lazy(
                    "view_comment",
                    kwargs={"vit_pk": comment.vit.pk, "pk": comment.pk},
                ),
            )
            if User.objects.get(username=result).profile.email_notif:
                subject = f"{comment.user.username.title()} mentioned you in a Comment."
                html_message = render_to_string(
                    "vit/email/comment_mention.html",
                    {
                        "from": comment.user,
                        "comment": comment,
                        "subject": subject,
                        "web_url": settings.WEB_HOST,
                    },
                )
                text_message = strip_tags(html_message)
                mail = EmailMultiAlternatives(
                    subject=subject,
                    body=text_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[User.objects.get(username=result).email],
                )
                mail.attach_alternative(html_message, "text/html")
                mail.send()


def find_embed_url(vit: Vit):
    """
    Find the Url in the Vit Create an embed
    Prams: vit
    """
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        vit.body,
    )
    for url in urls:
        client = requests.Session()
        try:
            res = client.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            if soup.find("meta", property="og:title"):
                embed = Embed.objects.get_or_create(url=url, vit=vit)[0]
                embed.title = soup.find("meta", property="og:title")["content"]
                if soup.find("meta", property="og:description"):
                    embed.description = soup.find(
                        "meta", property="og:description"
                    ).get("content", "")
                if soup.find("meta", property="og:image"):
                    embed.image_url = soup.find("meta", property="og:image")["content"]
                embed.save()
        except Exception as e:
            print(e)
            pass


def find_plustags(vit: Vit):
    for word in vit.body.split():
        if word[0] == "+" and word[1] != " ":
            plustag = Plustag.objects.get_or_create(name=word[1:].lower())
            vit.plustag.add(plustag[0])
