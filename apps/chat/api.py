import json
from django.http import JsonResponse

from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import ChatMessage, Chat
from apps.notification.utilities import create_notification


def send_message_api(request):
    if request.user.is_authenticated and request.method == "POST":
        data = json.loads(request.body)
        message = data["message"]
        chat = Chat.objects.get(pk=data["chat_id"])
        ChatMessage.objects.create(chat=chat, created_by=request.user, message=message)
        to_user = chat.users.exclude(pk=request.user.pk)[0]
        create_notification(
            verb="messaged",
            recipient=to_user,
            actor=request.user,
            object_type="chat",
            object_id=chat.id,
        )
        return JsonResponse({"status": "success", "message": message})
    return JsonResponse({"status": "error"})


def get_message_api(request):
    """
    A simple API to get the messages between the user.
    """
    if request.user.is_authenticated and request.method == "GET":
        to_user = get_object_or_404(User, username=request.GET["to_user"])
        chat = Chat.objects.filter(users__in=[request.user])
        chat = chat.filter(users__in=[to_user])
        chat_messages = ChatMessage.objects.filter(chat=chat[0])
        messages = []
        messages = list(
            chat_messages.values(
                "id",
                "message",
                "created_by__username",
                "created_at",
                "created_by__first_name",
                "created_by__last_name",
            )
        )
        # if len(messages) < 30:
        #     messages = messages
        # else:
        #     messages = messages[len(messages)-30:]
        context = {
            "status": "success",
            "chat": list(chat.values("id", "users", "modified_at")),
            "to_user": to_user.username,
            "messages": messages,
        }
        return JsonResponse(context)
    return JsonResponse({"status": "error"})
