from django.contrib import admin

from .models import Chat, ChatMessage

admin.site.register(Chat)
admin.site.register(ChatMessage)