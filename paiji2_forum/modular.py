from django.conf.urls import url, include

from modular_blocks import ModuleApp, TemplateTagBlock, modules

from . import urls


class ForumModule(ModuleApp):
    app_name = 'forum'
    name = 'forum'
    urls = url(r'^forum/', include(urls))
    templatetag_blocks = [
        TemplateTagBlock(
            name='forum',
            library='forum',
            tag='get_forum',
            cache_time=30,
            kwargs={
                'nb': 15,
            },
        ),
    ]


modules.register(ForumModule)
