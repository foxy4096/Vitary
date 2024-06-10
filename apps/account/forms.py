from django import forms
from django.contrib.auth.models import User
from apps.core.widgets import MarkdownWidget
from .models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "email_notif", "allow_nsfw", "use_gravatar"]
        widgets = {
            "bio": MarkdownWidget(),
        }


class UserProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar_image", "header_image"]


class UsernameForm(forms.Form):
    username = forms.CharField(
        max_length=30, required=True, help_text="Required.", label="Username"
    )

    class Meta:
        model = User
        fields = ["username"]


class DateOfBirthForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["date_of_birth"]
        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "id": "date_of_birth", "class": "input"}
            ),
        }
