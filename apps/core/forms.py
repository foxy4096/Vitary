from django import forms

from .models import Abuse

class ReportAbuseForm(forms.ModelForm):
    class Meta:
        model = Abuse
        fields = ['abuse_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'textarea','placeholder': 'Describe the abuse',
                                                                        'id': 'body'}),
        }
