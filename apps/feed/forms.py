from django import forms
from .models import Feed, Comment
from apps.core.widgets import MarkdownWidget

class FeedForm(forms.ModelForm):
    """
    Form for the Feed model
    """

    class Meta:
        model = Feed
        fields = ["body","nsfw"]
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
