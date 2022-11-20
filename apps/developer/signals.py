from django.db.models.signals import post_save
from django.dispatch import receiver


from django.contrib.auth.models import User
from .models import DevProfile, Token, Bot

@receiver(post_save, sender=DevProfile)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Bot)
def create_profile(sender, instance, created, **kwargs):
    if created:
        instance.user = User.objects.create(
            username=f"{instance.username.replace(' ', '')}{instance.id}",
            first_name=instance.name,
        )
        instance.user.save()
        instance.save()