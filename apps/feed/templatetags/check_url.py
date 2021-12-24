from django import template
from django.template.defaultfilters import stringfilter
import urllib.request
import urllib.error

register = template.Library()


@register.filter(name='check_url', is_safe=True)
@stringfilter
def check_url(value):
    my_list = value.split()
    for i in my_list:
        url = i.replace(',', '')
        if url.startswith('https://') or url.startswith('http://'):
            # j = f"<a href='http://{i.replace('https://', '').replace('https://', '')}'>{i}</a>"
            j = f"[{i}](http://{i.replace('https://', '').replace('https://', '')})"
            value = value.replace(i, j)
        else:
            pass
    return value
