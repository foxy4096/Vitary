from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.developer.models import Bot, DevProfile, Token


@receiver(post_save, sender=DevProfile)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(devprofile=instance)


@receiver(post_save, sender=Bot)
def create_profile(sender, instance, created, **kwargs):
    if created:
        instance.user = User.objects.create(
            username=f"{instance.username.replace(' ', '')}{instance.id}",
            first_name=instance.name,
        )
        instance.user.save()
        instance.save()
