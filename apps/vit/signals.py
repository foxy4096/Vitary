from django.dispatch import receiver
from django.db.models.signals import post_save


from .models import Vit, Comment
from apps.vit.utilities import (
    find_vit_mention,
    find_comment_mention,
    find_embed_url,
    find_plustags,
)


@receiver(post_save, sender=Vit)
def save_vit(sender, instance, created, **kwargs):
    if created:
        find_vit_mention(vit=instance)
        find_embed_url(vit=instance)
        find_plustags(vit=instance)


@receiver(post_save, sender=Comment)
def save_comment(sender, instance, created, **kwargs):
    if created:
        find_comment_mention(comment=instance)
