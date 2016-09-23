from __future__ import unicode_literals

from django.apps import AppConfig


class Paiji2ForumConfig(AppConfig):
    name = 'paiji2_forum'

    def ready(self):
        import update_db
        update_db.update_icons_db()
