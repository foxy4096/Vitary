from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify

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
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

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
            "image",
            "header_image",
            "email_notif",
            "allow_nsfw",
            "status",
        ]
        widgets = {
            "email_notif": forms.CheckboxInput(attrs={"class": "checkbox"}),
            "bio": forms.Textarea(
                attrs={
                    "class": "textarea",
                    "placeholder": "Tell us about yourself...,\nYou can use Markdown and mentions.",
                }
            ),
            "header_image": forms.FileInput(
                attrs={
                    "class": "input",
                    "style": """width: 100%;""",
                    "id": "header_image",
                }
            ),
            "image": forms.FileInput(
                attrs={"class": "input", "style": """width: 100%;""", "id": "image"}
            ),
            "status": forms.Select(
                attrs={"class": "select is-fullwidth", "style": """width: 100%;""", "id": "status"}
            ),
        }


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
                attrs={"type": "date", "id": "date_of_birth"}
            ),
        }