from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import User

class NotificationItemManager(models.Manager):
    def get_unread_count(self, user):
        return self.filter(notification__receiver=user, is_read=False).count()

    def get_notification_items_for(self, object_type, object_id):
        content_type = ContentType.objects.get_for_model(object_type)
        return self.select_related("notification").filter(
            content_type=content_type, object_id=object_id
        )

class Notification(models.Model):
    sender = models.ForeignKey(
        verbose_name=_("Sender"),
        to=User,
        on_delete=models.CASCADE,
        related_name="sender",
    )
    receiver = models.ForeignKey(
        verbose_name=_("Receiver"),
        to=User,
        on_delete=models.CASCADE,
        related_name="receiver",
    )
    verb = models.CharField(verbose_name=_("Verb"), max_length=255)
    is_read = models.BooleanField(verbose_name=_("Is Read"), default=False)
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    content_type = models.ForeignKey(
        verbose_name=_("Content Type"), to=ContentType, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"

    objects = NotificationItemManager()
