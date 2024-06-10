from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Chat, ChatMessage


@login_required()
def all_messages(request):
    if request.method == 'GET':
        chats = request.user.conversation_messages.all()
        chat_users = []
        for c in chats.all():
            chat_users.extend(u for u in c.users.all() if u != request.user)
        context = {
            'chat_users': set(chat_users),
        }
        return render(request, 'chat/all_messages.html', context)

@login_required
def redirect_to_chat(request, user_name):
    if request.method == 'GET':
        user = User.objects.get(username=user_name)
        chat = Chat.objects.filter(users__in=[request.user]).filter(users__in=[user])
        if chat.exists():
            chat = chat.first()
        else:
            chat = Chat.objects.create()
            chat.users.add(request.user)
            chat.users.add(user)
        return redirect('message_user_id', chat_id=chat.id)


@login_required
def message_user(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    chat_messages = ChatMessage.objects.filter(chat=chat).order_by('created_at')
    all_users = []
    for usr in chat.users.all():
        if usr != request.user:
            all_users.append(usr)
    to_user = all_users[0]
    context = {
        'to_user': to_user,
        'chat': chat,
        'chat_messages': chat_messages,
    }
    return render(request, 'chat/message_user.html', context)
