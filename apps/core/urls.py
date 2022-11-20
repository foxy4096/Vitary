from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.frontpage, name="home"),
    path("feed/", views.feed, name="feed"),
    path("users/", views.peoples, name="peoples"),
    path("explore/", views.explore, name="explore"),
    path("report/", views.report, name="report"),
    path("404/", views.page_404),
    path("search/", views.search, name="search"),
    path("badge/<int:pk>/", views.badge, name="badge"),
    path("dashboard/", views.redirect_to_profile, name="dashboard"),
]
