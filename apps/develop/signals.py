from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from django.contrib.auth.models import User
from .models import Bot


@receiver(post_save, sender=Bot)
def create_profile(sender, instance, created, **kwargs):
    if created:
        instance.user = User.objects.create(
            username=f"{instance.name.replace(' ', '')}{instance.id}",
            first_name=instance.name,
        )
        instance.user.save()
        instance.save()
