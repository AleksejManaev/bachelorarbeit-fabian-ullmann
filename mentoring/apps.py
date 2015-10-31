__author__ = 'ullmanfa'

from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'mentoring'

    def ready(self):
        import mentoring.signals
