from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    name = 'restaurants'
    verbose_name = 'Restauracje/Lokale'

    def ready(self):
        from . import signals
