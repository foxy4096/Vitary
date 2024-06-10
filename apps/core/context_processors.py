from random import choice

from django.conf import settings

from apps.feed.models import User, Feed
from .models import Alert
from .utilities import is_htmx_no_boost_request


def web_url(request):
    return {"web_url": settings.WEB_HOST}


def is_debug(request):
    return {"DEBUG": settings.DEBUG}


def random_color(request):
    colors = [
        "success",
        "danger",
        "warning",
        "black",
        "primary",
        "link",
        "info",
        "dark",
        "white",
        "light",
    ]
    return {"random_color": choice(colors)}


def frontpage_data(request):
    feed_count = Feed.objects.count()
    users_count = User.objects.count()
    latest_alert = Alert.objects.last()
    return {
        "feed_count": feed_count,
        "users_count": users_count,
        "latest_alert": latest_alert,
    }


def is_htmx(request):
    return {"is_htmx": is_htmx_no_boost_request(request)}
