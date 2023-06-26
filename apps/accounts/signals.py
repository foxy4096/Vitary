from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from django.contrib.auth.models import User
from .models import Profile

from allauth.account.signals import user_signed_up


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
