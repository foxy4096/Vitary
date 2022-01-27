from django import forms
from django.forms import ModelForm
from django import forms

from .models import Abuse, BadgeRequest, DonationProof

class ReportAbuseForm(ModelForm):
    class Meta:
        model = Abuse
        fields = ['abuse_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'textarea','placeholder': 'Describe the abuse',
                                                                        'id': 'body'}),
        }


class BadgeRequestForm(ModelForm):
    class Meta:
        model = BadgeRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'textarea','placeholder': 'Describe the abuse',
                                                                        'id': 'body'}),
        }


class DonationProofForm(ModelForm):
    class Meta:
        model = DonationProof
        fields = ['proof',]