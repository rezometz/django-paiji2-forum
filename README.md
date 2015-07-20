Forum
=====

URLconf
-------

For instance, in your project urls.py :

```
  url(r'^forum/', include('forum.urls', namespace='forum')),
```

`namespace='forum'` is mandatory.

Templates
---------

See `forum/templates/forum/base.html`.

You should change the name of the extended template (line 1) to fit to your project.

The extended template should have a "title" block, a "style" block to add a css file link, and a "content" block to show the main content.

User authentification model
---------------------------

`AUTH_USER_MODEL` should be defined in your project settings.py.

Icons static urls updating
--------------------------

Before using the forum (after the initial migration),
and every time you add an icon to forum/static/forum/icons,
you should execute, with `./manage.py shell` inside your project :

```
from forum import update_db
update_db.update_icons_db()
```

