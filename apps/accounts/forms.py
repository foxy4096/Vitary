from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'style': 'color: #b9b9b9;'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'style': 'color: #b9b9b9;'}),
            'username': forms.TextInput(attrs={'class': 'input', 'style': 'color: #b9b9b9;'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'style': 'color: #b9b9b9;'})
        }



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'email_notif')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'email_notif': forms.CheckboxInput(attrs={'class': 'checkbox'})
        }
