from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_detail, name="user_detail"),
    path("following/", views.user_following, name="following"),
    path("followers/", views.user_followers, name="followers"),
]
