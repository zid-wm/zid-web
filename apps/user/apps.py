from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'apps.user'

    def ready(self):
        from .update import start
        start()
