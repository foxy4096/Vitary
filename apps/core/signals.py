from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from django.core.mail import mail_managers
from django.urls import reverse
from apps.notification.utilities import notify


# @receiver(post_save, sender=Abuse)
# def create_abuse(sender, instance, created, **kwargs):
#     if created:
#         mail_managers(
#             subject='New Abuse',
#             message=f'{instance.user.username} has reported {instance.to_feed.user.username} for {instance.abuse_type} abuse.',
#             html_message=f'{instance.user.username} has reported {instance.to_feed.user.username} for {instance.abuse_type} abuse.'
#         )
#         if instance.to_feed.user != instance.user:
#             notify(message=f"{instance.user.username.title()} reported your feed: '{instance.to_feed.body}'", notification_type="abuse", to_user=instance.to_feed.user,
#                 by_user=instance.user, link=reverse('feed_detail', kwargs={'pk': instance.to_feed.id}))