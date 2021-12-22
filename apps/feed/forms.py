from django import forms
from .models import Feed


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ['body', 'image', 'video']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'input', 'style': '''width: 100%;
                                                                        height: 150px;
                                                                        padding: 12px 20px;
                                                                        box-sizing: border-box;
                                                                        border: px solid rgb(0, 0, 0);
                                                                        background-color: #ffffff;
                                                                        color: #b9b9b9;
                                                                        background-color : #4a4a4a; 
                                                                        resize: both;
            '''}),
        }
