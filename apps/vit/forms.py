from django import forms
from .models import Vit, Comment
from apps.core.widgets import MarkdownWidget

class VitForm(forms.ModelForm):
    """
    Form for the vit model
    """

    class Meta:
        model = Vit
        fields = ["body", "image", "video", "nsfw"]
        widgets = {
            "body": MarkdownWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": MarkdownWidget()
        }
