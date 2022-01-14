from django import forms
from django.forms import ModelForm
from django import forms

from .models import Abuse

class ReportAbuseForm(ModelForm):
    class Meta:
        model = Abuse
        fields = ['abuse_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'textarea','placeholder': 'Describe the abuse',
                                                                        'id': 'body'}),
        }