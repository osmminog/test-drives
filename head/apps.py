from django.apps import AppConfig
import os


class HeadConfig(AppConfig):
    name = 'head'
    verbose_name = "Тест драйвы"

    def ready(self):
        from . import parser_news, mixins

        if os.environ.get('RUN_HEAD', None) != 'true':
            parser_news.start_scheduler()
            mixins.start_scheduler()