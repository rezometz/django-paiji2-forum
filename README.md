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

You should change the name of the template extended (line 1) to fit to your project.

The extended template should have a "title" block, a "style" block to add a css file link, and a "content" block to show the main content.

User authentification model
---------------------------

`AUTH_USER_MODEL` should be defined in your project settings.py.
