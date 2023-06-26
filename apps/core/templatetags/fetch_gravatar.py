import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def gravatar_url(user, size=100):
    return f"http://www.gravatar.com/avatar/{hashlib.md5(user.email.lower().encode()).hexdigest()}?s={size}"
    # return "http://localhost:8000/media/uploads/default.jpg"