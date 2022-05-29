import json
from django.http import JsonResponse

from django.urls import reverse
from django.contrib.auth.models import User
from apps.notification.utilities import notify
from .models import ChatMessage, Chat
from apps.notification.utilities import notify


def send_message_api(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            message = data["message"]
            chat = Chat.objects.get(pk=data["chat_id"])
            ChatMessage.objects.create(
                chat=chat, created_by=request.user, message=message
            )
            to_user = chat.users.exclude(pk=request.user.pk)[0]
            notify(
                message=f"{request.user.get_full_name()} sent you a message",
                notification_type='message',
                to_user=to_user,
                by_user=request.user,
                link=reverse('message_user', kwargs={'user_name': to_user.username}),
                )
            return JsonResponse({"status": "success", "message": message})
        return JsonResponse({"status": "error"})
    else:
        return JsonResponse({"status": "error"})


def get_message_api(request):
    """
    A simple API to get the messages between the user.
    """
    if request.user.is_authenticated:
        if request.method == "GET":
            to_user = User.objects.get(username=request.GET["to_user"])
            chat = Chat.objects.filter(users__in=[request.user])
            chat = chat.filter(users__in=[to_user])
            chat_messages = ChatMessage.objects.filter(chat=chat[0])
            messages = []
            messages = list(chat_messages.values("id", "message", "created_by__username", "created_at", "created_by__first_name", "created_by__last_name"))
            # if len(messages) < 30:
            #     messages = messages
            # else:
            #     messages = messages[len(messages)-30:]
            context = {
                "status": "success",
                "chat": list(chat.values("id", "users", "modified_at")),
                "to_user": to_user.username,
                "messages": messages
            }
            return JsonResponse(context)
        return JsonResponse({"status": "error"})
    else:
        return JsonResponse({"status": "error"})
