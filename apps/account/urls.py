from django.urls import path, include

from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", views.signup, name="signup"),
    path("userprofile/", views.edit_userprofile, name="edit_userprofile"),
    path("userprofile/advance/", views.advanced_settings, name="advance_settings"),
    path("userprofile/advance/delete/", views.delete_account, name="delete_account"),
    path(
        "userprofile/advance/change_username/",
        views.change_username,
        name="change_username",
    ),
]
