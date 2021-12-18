from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='conversation_messages')
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_at']


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message')

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        self.chat.save()

        super().save(*args, **kwargs)