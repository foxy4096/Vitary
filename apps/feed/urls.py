from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_feed, name="add_feed"),
    path("<int:pk>/", views.feed_detail, name="feed_detail"),
    path("<int:pk>/delete/", views.delete_feed, name="delete_feed"),
    path("<int:feed_pk>/likes/", views.feed_liked_users, name="feed_liked_users"),
    path("<int:feed_pk>/like/", views.like_feed, name="like_feed"),
    path(
        "<int:feed_pk>/comment/view/<int:pk>/", views.view_comment, name="view_comment"
    ),
    path("comment/_form/", views._comment_form, name="_comment_form"),
    path("comment/_refresh/<int:pk>/", views.comment_refresh, name="_comment_refresh"),
]
