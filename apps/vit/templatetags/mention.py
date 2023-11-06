from django import template
from django.urls import reverse
from ..models import User
import re

register = template.Library()


@register.filter
def mention(value):
    mention_pattern = r"@(\w+)"

    def replace_mention(match):
        username = match.group(1)
        user = User.objects.filter(username=username).first()
        if user:
            profile_url = reverse("user_detail", args=[username])
            mention_link = (
                f'<a href="{profile_url}" class="user-mention" title="{username}">@{username}</a>'
            )
            return mention_link
        return match.group(0)

    return re.sub(mention_pattern, replace_mention, value)
