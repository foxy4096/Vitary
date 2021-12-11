from django.db import models

from apps.accounts.models import Profile


class Notification(models.Model):
    """
    This class represents the Notification model.
    """
    NOTIFICATION_TYPES = [
        ('mention', 'Mention'),
        ('comment', 'Comment'),
        ('like', 'Like'),
        ('follow', 'Follow'),
    ]
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES)
    to_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='to_user')
    by_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='by_user')
    link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.message