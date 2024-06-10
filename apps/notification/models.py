from django.db import models

from apps.account.models import User, get_sentinel_user


class Notification(models.Model):
    recipient = models.ForeignKey(
        User, related_name="notifications", on_delete=models.SET(get_sentinel_user)
    )
    actor = models.ForeignKey(User, related_name="+", on_delete=models.SET(get_sentinel_user))
    verb = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    object_type = models.CharField(max_length=255)
    object_id = models.PositiveBigIntegerField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.actor.username} → {self.recipient.username}"
    
    def notification_message(self):
        if self.verb == "commented":
            return f"{self.actor.username} commented on your post"
        elif self.verb == "like":
            return f"{self.actor.username} liked your post"
        elif self.verb == "followed":
            return f"{self.actor.username} started following you"
        else:
            return "Unknown notification type"
