from django import forms
from .models import Vit, Comment


class VitForm(forms.ModelForm):
    """
    Form for the vit model
    """

    class Meta:
        model = Vit
        fields = ["body", "image", "video", "nsfw"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "placeholder": "What's on your mind?",
                    "style": """height: 150px;""",
                    "id": "body",
                    "onKeyup": "processChange()",
                }
            ),
            "nsfw": forms.CheckboxInput(attrs={"id": "nsfw"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
