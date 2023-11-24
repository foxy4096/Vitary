from django.apps import AppConfig


class VitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.feed'

    def ready(self):
        from . import signals
