import re

from django.conf import settings
from django.urls import reverse_lazy

from django.template.loader import render_to_string
from apps.notification.utilities import notify

from django.contrib.auth.models import User

from apps.vit.models import Plustag
from django.core.mail import EmailMessage


def find_mention(request, vit):
    """
    Find the Mention in the Vit then Create A Notification
    Prams: request and vit
    """

    results = re.findall("(^|[^@\w])@(\w{1,150})", vit.body)

    for result in results:
        result = result[1]

        if User.objects.filter(username=result).exists() and result != request.user.username:

            notify(
                message=f"""{request.user.username.title()} Mentioned You in a Vit - '{vit.body}'""",
                notification_type="mention",
                to_user=User.objects.get(username=result),
                by_user=request.user,
                link=reverse_lazy('vit_detail', kwargs={
                                  'pk': vit.pk})
            )

            if User.objects.get(username=result).profile.email_notif:

                msg = render_to_string(
                    'vit/email/mention.html',
                    {
                        'from': request.user,
                        'vit': vit
                    }
                )

                subject = f"{request.user.username.title()} mentioned you in a Vit.",
                mail = EmailMessage(subject=subject,
                                    body=msg,
                                    from_email=settings.DEFAULT_FROM_EMAIL,
                                    to=[User.objects.get(username=result).email],
                                    )
                mail.send()


def find_plustag(vit):
    """
    Find the Plustag in a Vit and create a plustag object
    Prams: vit
    """
    results = vit.body.split()
    for word in results:
        if word[0] == '+' and word[1] != ' ':
            plustag = Plustag.objects.get_or_create(name=word[1:])
            vit.plustag.add(plustag[0])
            vit.save()
    
    return

