paiji2-forum
============

License
-------

Affero GPL v3

Requirements
------------

You must have django-bootstrap3 installed, and a user authentication model.

URLconf
-------

For instance, in your project urls.py :

```
  url(r'^forum/', include('paiji2_forum.urls', namespace='forum')),
```

`namespace='forum'` is mandatory.

Templates
---------

See `paiji2_forum/templates/forum/base.html`.

You should change the name of the extended template (line 1) to fit to your project.

The extended template should have a "title" block, a "style" block to add a css file link, and a "content" block to show the main content.

Translations
------------

The default language is english. French and german translations are provided. Please forgive my mistakes :-)
