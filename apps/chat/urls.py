from django.urls import path

from . import views

urlpatterns = [
    path('m/<str:user_name>/', views.redirect_to_chat, name='message_user'),
    path('message/<int:chat_id>/', views.message_user, name='message_user_id'),
    path('m/', views.all_messages, name='all_messages'),
]