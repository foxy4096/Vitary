from django.apps import AppConfig


class DeveloperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.developer'

    def ready(self):
        from . import signals