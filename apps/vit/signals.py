from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.vit.models import Vit
from apps.vit.utilities import (
    find_plustags,
    find_vit_mention,
)
from apps.vit.tasks import find_embed_url


@receiver(post_save, sender=Vit)
def save_vit(sender, instance, created, **kwargs):
    if created:
        find_embed_url(instance.id)
        find_vit_mention(vit=instance)
        find_plustags(vit=instance)
