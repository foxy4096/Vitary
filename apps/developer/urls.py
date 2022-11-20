from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="developer_home"),
    path("join/", views.join, name="developer_join"),
    path("dashboard/", views.dashboard, name="developer_dashboard"),
    path("token/refresh", views.refresh_token, name="refresh_token"),

    # Bot
    path('bot/create/', views.bot_create, name='developer_bot_create'),
    path('bot/<int:id>/', views.bot_detail, name='developer_bot_detail'),
    path('bot/<int:id>/delete/', views.bot_delete, name='developer_bot_delete'),
    path('bot/<int:id>/webhook/create/', views.webhook_create, name='webhook_create'),
    path('bot/<int:id>/webhook/<int:webhook_id>/delete/', views.webhook_delete, name='webhook_delete'),
    path('bot/<int:id>/webhook/<int:webhook_id>/edit/', views.webhook_edit, name='webhook_edit'),
]
