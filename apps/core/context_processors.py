from django.conf import settings
from random import choice

def web_url(request):
    return {'web_url': settings.WEB_HOST}

def is_debug(request):
    return {'DEBUG': settings.DEBUG}

def random_color(request):
    colors = ["success", "danger", "warning", "black", "primary", "link", "info", "dark", "white", "light"]
    return {'random_color': choice(colors)}