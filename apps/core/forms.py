from django import forms

from .models import Abuse

class ReportAbuseForm(forms.ModelForm):
    class Meta:
        model = Abuse
        fields = ['abuse_type', 'description']