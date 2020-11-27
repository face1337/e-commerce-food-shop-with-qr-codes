from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    name = 'restaurants'

    def ready(self):
        from . import signals
