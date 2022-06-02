import json
import re
import requests
from bs4 import BeautifulSoup
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

from django.urls import reverse_lazy

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.auth.models import User
from .models import Vit, Plustag, Comment, Embed

from apps.notification.utilities import notify


@receiver(post_save, sender=Vit)
def save_vit(sender, instance, created, **kwargs):
    body = instance.body
    user = instance.user
    results = body.split()
    # Save Plustag
    for word in results:
        if word[0] == "+" and word[1] != " ":
            plustag = Plustag.objects.get_or_create(name=word[1:])
            instance.plustag.add(plustag[0])

    # Save Embed
    # urls = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", body)
    # try:
    #     for url in urls:
    #         embed = Embed.objects.get_or_create(url=url, vit=instance)[0]
    #         res = requests.get(url)
    #         soup = BeautifulSoup(res.text, "html.parser")
    #         if soup.find("meta", property="og:title"):
    #             embed.title = soup.find("meta", property="og:title")["content"]
    #         if soup.find("meta", property="og:description"):
    #             embed.description = soup.find("meta", property="og:description")["content"]
    #         if soup.find("meta", property="og:image"):
    #             embed.image_url = soup.find("meta", property="og:image")["content"]
    #         embed.save()
    # except:
    #     pass
    # Save Mention
    if created:
        results = re.findall("(^|[^@\w])@(\w{1,150})", body)
        for result in results:
            result = result[1]
            if (
                User.objects.filter(username=result).exists()
                and result != user.username
            ):
                instance.mentions.add(User.objects.get(username=result))
                notify(
                    message=f"""{user.username.title()} Mentioned You in a Vit: {body}""",
                    notification_type="mention",
                    to_user=User.objects.get(username=result),
                    by_user=user,
                    link=reverse_lazy("vit_detail", kwargs={"pk": instance.pk}),
                )

                if User.objects.get(username=result).profile.email_notif:
                    subject = f"{user.username.title()} mentioned you in a Vit."
                    html_message = render_to_string(
                        "vit/email/vit_mention.html",
                        {
                            "from": user,
                            "vit": instance,
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

            try:
                if User.objects.get(username=result).bot:
                    print("Bot")
                    bot_user = User.objects.get(username=result)
                    webhooks = bot_user.bot.webhook_set.all()
                    print(webhooks)
                    for webhook in webhooks:
                        print(webhook.event_type)
                        if webhook.event_type == "on_vit_mention":
                            print("Till Here")
                            if webhook.method == "GET":
                                res = requests.get(
                                    webhook.payload_url,
                                    data=json.dumps({
                                        "from": user.username,
                                        "vit": instance.pk,
                                        "body": body,
                                    }),
                                    headers={
                                        "Authorization": f"Key {webhook.bot.private_key}"
                                        if webhook.required_authentication
                                        else "",
                                        "Content-Type": webhook.content_type,
                                    },
                                )
                            elif webhook.method == "POST":
                                res = requests.post(
                                    webhook.payload_url,
                                    data=json.dumps({
                                        "from": user.username,
                                        "vit": instance.pk,
                                        "body": body,
                                    }),
                                    headers={
                                        "Authorization": f"Key {webhook.bot.private_key}"
                                        if webhook.required_authentication
                                        else "",
                                        "Content-Type": webhook.content_type,
                                    },
                                )
                            if res.status_code == 200:
                                bot_user.profile.status = "online"
                                bot_user.profile.save()
                            else:
                                bot_user.profile.status = "away"
                                bot_user.profile.save()
            except:
                pass


@receiver(post_save, sender=Comment)
def save_comment(sender, instance, **kwargs):
    body = instance.body
    user = instance.user
    results = body.split()
    # Save Plustag
    for word in results:
        if word[0] == "+" and word[1] != " ":
            plustag = Plustag.objects.get_or_create(name=word[1:])
            instance.plustag.add(plustag[0])
            instance.save()
    # Save Mention
    results = re.findall("(^|[^@\w])@(\w{1,150})", body)
    for result in results:
        result = result[1]
        if (
            User.objects.filter(username=result).exists()
            and result != user.username
        ):
            notify(
                message=f"""{user.username.title()} Mentioned You in a Comment: {body}""",
                notification_type="mention",
                to_user=User.objects.get(username=result),
                by_user=user,
                link=reverse_lazy(
                    "view_comment",
                    kwargs={"vit_pk": instance.vit.pk, "pk": instance.pk},
                ),
            )
            if User.objects.get(username=result).profile.email_notif:
                subject = f"{user.username.title()} mentioned you in a Comment."
                html_message = render_to_string(
                    "vit/email/comment_mention.html",
                    {
                        "from": user,
                        "comment": instance,
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
            try:
                if User.objects.get(username=result).bot:
                    bot_user = User.objects.get(username=result)
                    webhooks = bot_user.bot.webhook_set.all()
                    for webhook in webhooks:
                        if webhook.event_type == "on_comment_mention":
                            try:
                                if webhook.method == "GET":
                                    res = requests.get(
                                        webhook.payload_url,
                                        data=json.dumps({
                                            "from": user.username,
                                            "comment": instance.pk,
                                            "body": body,
                                        }),
                                        headers={
                                            "Authorization": f"Key {webhook.bot.private_key}"
                                            if webhook.required_authentication
                                            else "",
                                            "Content-Type": webhook.content_type,
                                        },
                                    )
                                elif webhook.method == "POST":
                                    res = requests.post(
                                        webhook.payload_url,
                                        data=json.dumps({
                                            "from": user.username,
                                            "comment": instance.pk,
                                            "body": body,
                                        }),
                                        headers={
                                            "Authorization": f"Key {webhook.bot.private_key}"
                                            if webhook.required_authentication
                                            else "",
                                            "Content-Type": webhook.content_type,
                                        },
                                    )
                                if res.status_code == 200:
                                    bot_user.profile.status = "online"
                            except:
                                bot_user.profile.status = "away"
                            bot_user.profile.save()
            except:
                pass