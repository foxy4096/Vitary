from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Chat, ChatMessage

@login_required
def message_user(request, username):
    to_user = User.objects.get(username=username)
    if to_user == request.user:
        return redirect('home')
    chat = Chat.objects.filter(users__in=[request.user])
    chat = chat.filter(users__in=[to_user])

    if chat.count() == 1:
        chat = chat[0]
    else:
        chat = Chat.objects.create()
        chat.users.add(request.user)
        chat.users.add(to_user)
        chat.save()
    chat_messages =ChatMessage.objects.filter(chat=chat)
    context = {
        'to_user': to_user,
        'chat': chat,
        'chat_messages': chat_messages,
    }
    return render(request, 'chat/message_user.html', context)

