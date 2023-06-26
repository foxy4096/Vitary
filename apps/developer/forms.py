from django import forms

from apps.accounts.models import Profile

from apps.developer.models import Bot, DevProfile, WebHook


class DevProfileCreateForm(forms.ModelForm):
    class Meta:
        model = DevProfile
        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class DevProfileForm(forms.ModelForm):
    class Meta:
        model = DevProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "bio",
            "github_username",
            "twitter_username",
            "website",
        ]


class BotCreationForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        help_text="Enter the name of your bot. This will be displayed on it's profile.",
    )
    username = forms.CharField(
        max_length=100,
        help_text="Enter the username of your bot. This will be used to identify your bot on the platform.",
    )

    class Meta:
        model = Bot
        fields = [
            "name",
            "username",
        ]


class BotEditForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ["name", "description"]


class BotUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "header_image", "status"]
        widgets = {
            "header_image": forms.FileInput(
                attrs={
                    "class": "input",
                    "style": """width: 100%;""",
                    "id": "header_image",
                }
            ),
        }


class WebHookForm(forms.ModelForm):
    class Meta:
        model = WebHook
        fields = [
            "name",
            "description",
            "payload_url",
            "event_type",
            "method",
            "content_type",
            "required_authentication",
        ]
