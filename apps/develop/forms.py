from django import forms

from .models import DevProfile

class DevProfileCreateForm(forms.ModelForm):
    class Meta:
        model = DevProfile
        fields = ['first_name', 'last_name', 'email',]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input is-medium is-info', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input is-medium is-info', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'input is-medium is-info', 'placeholder': "Email"}),
        }

class DevProfileForm(forms.ModelForm):
    class Meta:
        model = DevProfile
        fields = ['first_name', 'last_name', 'email', 'bio', 'github_username', 'twitter_username', 'website']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input is-info', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input is-info', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'input is-info', 'placeholder': "Email"}),
            'github_username': forms.TextInput(attrs={'class': 'input is-info', 'placeholder': 'Github Username 🐱‍👤'}),
            'twitter_username': forms.TextInput(attrs={'class': 'input is-info', 'placeholder': 'Twitter Username 🦅'}),
            'website': forms.TextInput(attrs={'class': 'input is-info', 'placeholder': 'Website 🌎'}),
            'bio': forms.Textarea(attrs={'class': 'textarea is-info', 'placeholder': 'Bio 📝'}),
        }