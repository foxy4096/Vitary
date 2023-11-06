from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from apps.core.widgets import MarkdownWidget
from .models import Profile


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text="Required.", label="First Name"
    )
    last_name = forms.CharField(
        max_length=30, required=False, help_text="Optional.", label="Last Name"
    )
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")

        if commit:
            user.save()

        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "bio",
            "email_notif",
            "allow_nsfw",
            "dark_mode",
            "status",
            "use_gravatar"
        ]
        widgets = {
            "bio": MarkdownWidget(),
        }


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "header_image"]

class UsernameForm(forms.Form):
    username = forms.CharField(
        max_length=30, required=True, help_text="Required.", label="Username"
    )

    class Meta:
        model = User
        fields = ["username"]


class DateOfBirthForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth"]
        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "id": "date_of_birth", "class": "input"}
            ),
        }
