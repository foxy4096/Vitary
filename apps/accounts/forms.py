from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

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
