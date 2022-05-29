from django.apps import AppConfig


class DevelopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.develop'

    def ready(self):
        from . import signals
