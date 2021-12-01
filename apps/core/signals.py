from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from django.conf import settings

from apps.core.models import Comment

@receiver(post_save, sender=Comment)
def send_notification_mail(sender, created, instance, **kwargs):
    if created:
        if instance.created_by.user.is_staff and instance.created_by.user.email:
            if instance.issue.created_by.user.email:
                send_mail(
                    subject=f"{instance.created_by.user.username.title()} commented on your issue.",
                    message=f"""
                    {instance.created_by.user.username.title()} wrote \n
                    {instance.comment}\n
                    You are reciving this email because you have opened a issue on our site.""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.issue.created_by.user.email],
                    fail_silently=False
                )
