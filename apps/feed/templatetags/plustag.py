from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from ..models import Plustag

register = template.Library()


@register.filter(name='plustag', is_safe=True)
@stringfilter
def plustag(value):
    val = value.split()
    for i in val:
        if i[0] == '+':
            try:
                stng = i[1:].replace(',', '').replace('.', '').replace('!', '').replace('?', '').replace(';', '').replace(':', '').replace('-', '').replace('_', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace(
                '/', '').replace('\\', '').replace('*', '').replace('=', '').replace('%', '').replace('$', '').replace('#', '').replace('^', '').replace('&', '').replace('|', '').replace('~', '').replace('`', '').replace('<', '').replace('>', '').replace("'", "")
                plustag = Plustag.objects.get_or_create(name=stng)[0]
                plustag_link = reverse_lazy('plustag_feeds', kwargs={'p': plustag.name})
                j = f"<a href='{plustag_link}'><b>{i}</b></a>"
                value = value.replace(i, j)
            except:
                pass
    return value

