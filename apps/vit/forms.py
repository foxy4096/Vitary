from django import forms
from .models import Vit


class VitForm(forms.ModelForm):
    class Meta:
        model = Vit
        fields = ['body', 'image', 'video']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'input', 'placeholder': 'What\'s on your mind?', 'id': 'body'}),
            'image': forms.FileInput(attrs={'class': 'file-input', 'style': '''width: 100%;''', 'id': 'image'}),
            'video': forms.FileInput(attrs={'class': 'file-input', 'style': '''width: 100%;''', 'id': 'video'}),
        }
