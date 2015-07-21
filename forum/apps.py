from django.apps import AppConfig

class ForumConfig(AppConfig):

    name = 'forum'
    verbose_name = 'forum'

    def ready(self):
       from forum import update_db
       update_db.update_icons_db()
