from django import forms

from apps.core.models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            "url",
            "description",
            "report_type",
        ]
