from django import forms
from .models import Vit, Comment


class VitForm(forms.ModelForm):
    """
    Form for the vit model
    """
    class Meta:
        model = Vit
        fields = ['body', 'image', 'video', 'nsfw']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'What\'s on your mind?', 'id': 'body'}),
            'image': forms.FileInput(attrs={'class': 'input', 'style': '''width: 100%;''', 'id': 'image'}),
            'video': forms.FileInput(attrs={'class': 'input', 'style': '''width: 100%;''', 'id': 'video', 'accept': 'video/*'}),
            'nsfw': forms.CheckboxInput(attrs={'id': 'nsfw'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']