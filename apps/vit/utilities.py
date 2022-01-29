import re

from django.conf import settings
from django.urls import reverse_lazy

from django.template.loader import render_to_string
from apps.notification.utilities import notify

from django.contrib.auth.models import User

from apps.vit.models import Plustag
from django.core.mail import EmailMultiAlternatives


def find_mention(request, ntype, **kwargs):
    """
    Find the Mention in the Vit or Comment then Create A Notification also send an email to the mentioned user
    Prams: request, ntype and vit or comment
    """

    # For Vit
    if ntype == 'vit':

        results = re.findall("(^|[^@\w])@(\w{1,150})", kwargs["vit"].body)

        for result in results:
            result = result[1]

            if User.objects.filter(username=result).exists() and result != request.user.username:

                notify(
                    message=f"""{request.user.username.title()} Mentioned You in a Vit - '{kwargs["vit"].body}'""",
                    notification_type="mention",
                    to_user=User.objects.get(username=result),
                    by_user=request.user,
                    link=reverse_lazy('vit_detail', kwargs={
                                    'pk': kwargs["vit"].pk})
                )
                kwargs["vit"].mentions.add(User.objects.get(username=result))

                if User.objects.get(username=result).profile.email_notif:

                    msg = render_to_string(
                        'vit/email/mention.html',
                        {
                            'from': request.user,
                            'vit': kwargs["vit"],
                        }
                    )

                    subject = f"{request.user.username.title()} mentioned you in a Vit.",
                    mail = EmailMultiAlternatives(subject=subject,
                                        body=msg,
                                        from_email=settings.DEFAULT_FROM_EMAIL,
                                        to=[User.objects.get(username=result).email],
                                        )
                    mail.send()
    
    # For Comment
    elif ntype == 'comment':
        results = re.findall("(^|[^@\w])@(\w{1,150})", kwargs["comment"].body)

        for result in results:
            result = result[1]

            if User.objects.filter(username=result).exists() and result != request.user.username:

                notify(
                    message=f"""{request.user.username.title()} Mentioned You in a Comment - '{kwargs["comment"].body}'""",
                    notification_type="mention",
                    to_user=User.objects.get(username=result),
                    by_user=request.user,
                    link=reverse_lazy('vit_detail', kwargs={
                                    'pk': kwargs["comment"].vit.pk})
                )

                if User.objects.get(username=result).profile.email_notif:

                    msg = render_to_string(
                        'vit/email/mention.html',
                        {
                            'from': request.user,
                            'comment': kwargs["comment"],
                        }
                    )

                    subject = f"{request.user.username.title()} mentioned you in a Comment.",
                    mail = EmailMultiAlternatives(subject=subject,
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

