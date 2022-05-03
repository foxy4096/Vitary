from django import forms

from .models import DevProfile

class DevProfileCreateForm(forms.ModelForm):
    class Meta:
        model = DevProfile
        fields = ['first_name', 'last_name', 'email',]

class DevProfileForm(forms.ModelForm):
    class Meta:
        model = DevProfile
        fields = ['first_name', 'last_name', 'email', 'bio', 'github_username', 'twitter_username', 'website']