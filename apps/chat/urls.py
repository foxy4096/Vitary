from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>/', views.message_user, name='message_user'),
]