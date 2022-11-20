from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.auth.models import User
from django.urls import reverse_lazy

register = template.Library()


@register.filter(name='mention', is_safe=True)
@stringfilter
def mention(value):
    my_list = value.split()
    for i in my_list:
        if i[0] == '@':
            try:
                stng = i[1:].replace(',', '').replace('.', '').replace('!', '').replace('?', '').replace(';', '').replace(':', '').replace('-', '').replace('_', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace(
                    '/', '').replace('\\', '').replace('*', '').replace('#', '').replace('=', '').replace('%', '').replace('$', '').replace('^', '').replace('&', '').replace('|', '').replace('~', '').replace('`', '').replace('<', '').replace('>', '').replace("'", "")
                user = User.objects.get(username=stng)
                if user:
                    profile_link = reverse_lazy('profile_view', kwargs={
                                                'username': user.username})
                    j = f"<a href='{profile_link}' data-toggle='tooltip' title='{user.username}'><b>{i}</b></a>"
                    value = value.replace(i, j)
            except User.DoesNotExist:
                pass

    return value
