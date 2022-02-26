from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify

from .models import Profile, Group

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.', label='First Name')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label='Last Name')
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': "Last Name"}),
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}),
        }


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
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': "Last Name"}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}),
        }



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'header_image', 'bio','email_notif')
        widgets = {
            'email_notif': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'bio': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Tell us about yourself...,\n You can use Markdown and mentions.'}),
            'header_image': forms.FileInput(attrs={'class': 'input', 'style': '''width: 100%;''', 'id': 'header_image'}),
            'image': forms.FileInput(attrs={'class': 'input', 'style': '''width: 100%;''', 'id': 'image'}),
        }

class UsernameForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, help_text='Required.', label='Username')
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}),
        }
        

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'image', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Group Name'}),
            'description': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Group Description'}),
            'image': forms.FileInput(attrs={'class': 'input', 'placeholder': 'Group Image'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }

        def save(self, commit=True):
            group = super().save(commit=False)
            group.name = self.cleaned_data['name']
            group.description = self.cleaned_data['description']
            if commit:
                group.slug = slugify(group.name)
                group.save()
            return group
