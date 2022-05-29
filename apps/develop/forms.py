from django import forms

from .models import DevProfile, Bot, WebHook
from apps.accounts.models import Profile

class DevProfileCreateForm(forms.ModelForm):
    class Meta:
        model = DevProfile
        fields = ['first_name', 'last_name', 'email',]

class DevProfileForm(forms.ModelForm):
    class Meta:
        model = DevProfile
        fields = ['first_name', 'last_name', 'email', 'bio', 'github_username', 'twitter_username', 'website']


class BotCreationForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['name',]

class BotEditForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['name', 'description']

class BotUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'header_image']
        widgets = {
            'header_image': forms.FileInput(attrs={'class': 'input', 'style': '''width: 100%;''', 'id': 'header_image'}),
            'image': forms.FileInput(attrs={'class': 'input', 'style': '''width: 100%;''', 'id': 'image'}),
        }

class WebHookForm(forms.ModelForm):
    class Meta:
        model = WebHook
        fields = ['name', 'description', 'payload_url', 'event_type', 'method', 'content_type', 'required_authentication']