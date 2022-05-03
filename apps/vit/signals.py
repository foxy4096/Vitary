import re
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

from django.urls import reverse_lazy

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.auth.models import User
from .models import Vit, Plustag, Comment

from apps.notification.utilities import notify


@receiver(post_save, sender=Vit)
def save_vit(sender, instance, **kwargs):
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
            instance.mentions.add(User.objects.get(username=result))
            notify(
                message=f"""{user.username.title()} Mentioned You in a Vit: {body}""",
                notification_type="mention",
                to_user=User.objects.get(username=result),
                by_user=user,
                link=reverse_lazy("vit_detail", kwargs={"pk": instance.pk}),
            )
            # Send Email if email notification is enabled
            if User.objects.get(username=result).profile.email_notif:
                subject = f"{user.username.title()} mentioned you in a Vit."
                html_message = render_to_string(
                    "vit/email/vit_mention.html",
                    {
                        "from": user,
                        "vit": instance,
                        "subject": subject,
                        "web_url": settings.WEB_HOST
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
                link=reverse_lazy("view_comment", kwargs={"vit_pk": instance.vit.pk, "pk": instance.pk}),
            )
            # Send Email if email notification is enabled
            if User.objects.get(username=result).profile.email_notif:
                subject = f"{user.username.title()} mentioned you in a Comment."
                html_message = render_to_string(
                    "vit/email/comment_mention.html",
                    {
                        "from": user,
                        "comment": instance,
                        "subject": subject,
                        "web_url": settings.WEB_HOST
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