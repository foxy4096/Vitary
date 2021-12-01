from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_feed, name='add_feed'),
    path('<int:pk>/', views.feed_detail, name='feed_detail'),
    path('<int:pk>/edit/', views.edit_feed, name='edit_feed'),
    path('<int:pk>/delete/', views.delete_feed, name='delete_feed'),
    path('add_comment/', views.add_comment, name='add_comment'),
]