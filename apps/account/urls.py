from django.urls import path, include

from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("userprofile/", views.EditUserProfileView.as_view(), name="edit_userprofile"),
    path("userprofile/advance/", views.AdvancedSettingsView.as_view(), name="advance_settings"),
    path("userprofile/advance/delete/", views.DeleteAccountView.as_view(), name="delete_account"),
    path(
        "userprofile/advance/change_username/",
        views.ChangeUsernameView.as_view(),
        name="change_username",
    ),
]
