from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class CmdbConfig(AppConfig):
    name = 'cmdb'


class SuitConfig(DjangoSuitConfig):
    # layout = 'horizontal'
    layout = 'vertical'
