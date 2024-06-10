from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserDetailView.as_view(), name="user_detail"),
    path("following/", views.UserFollowingView.as_view(), name="following"),
    path("followers/", views.UserFollowersView.as_view(), name="followers"),
]
