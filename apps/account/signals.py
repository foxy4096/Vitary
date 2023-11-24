from django.db.models.signals import post_save, post_migrate
from django.dispatch.dispatcher import receiver

from django.contrib.auth.models import User
from .models import UserProfile, get_sentinel_user


@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_migrate)
def create_ghost_user(sender, **kwargs):
    get_sentinel_user()
