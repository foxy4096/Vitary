from django.conf import settings

def web_url(request):
    return {'web_url': settings.WEB_HOST}