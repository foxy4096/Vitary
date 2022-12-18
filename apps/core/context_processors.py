from django.conf import settings
from random import choice
from apps.vit.models import Vit, User
from apps.developer.models import DevProfile


def web_url(request):
    return {'web_url': settings.WEB_HOST}

def is_debug(request):
    return {'DEBUG': settings.DEBUG}

def random_color(request):
    colors = ["success", "danger", "warning", "black", "primary", "link", "info", "dark", "white", "light"]
    return {'random_color': choice(colors)}

def frontpage_data(request):
    vit_count = Vit.objects.count()
    users_count = User.objects.count()
    dev_count = DevProfile.objects.count()
    return {'vit_count': vit_count, 'users_count': users_count, 'dev_count': dev_count}