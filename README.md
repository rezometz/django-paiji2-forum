paiji2-forum
============


[![Build Status](https://travis-ci.org/rezometz/django-paiji2-forum.svg?branch=master)](https://travis-ci.org/rezometz/django-paiji2-forum)
[![Code Climate](https://codeclimate.com/github/rezometz/django-paiji2-forum/badges/gpa.svg)](https://codeclimate.com/github/rezometz/django-paiji2-forum)
[![Coverage Status](https://coveralls.io/repos/rezometz/django-paiji2-forum/badge.svg?branch=master&service=github)](https://coveralls.io/github/rezometz/django-paiji2-forum?branch=master)

License
-------

[![Affero GPL v3](http://www.gnu.org/graphics/agplv3-88x31.png)](http://www.gnu.org/licenses/agpl-3.0.html)

Testing
-------

In the root of this folder, you can execute:
```
pip install -U .
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Requirements
------------

You must have `django-bootstrap3` and `django-mptt` installed.
`django-html-validator` is required for testing purposes.

URLconf
-------

For instance, in the `urls.py` of your project:

```
  url(r'^forum/', include('paiji2_forum.urls')),
```

Templates
---------

See `paiji2_forum/templates/forum/base.html` for an example.

You should change the name of the extended template (line 1) to fit to your project.

The extended template should have a "title" block, a "style" block to add a css file link, and a "content" block to show the content of the forum.

It must also link to "bootstrap.css" or "bootstrap.min.css" (bootstrap version 3), for instance with:
```
<link rel="stylesheet" type="text/css" href="https://unpkg.com/bootstrap@3/dist/css/bootstrap.min.css"/>
```

Translations
------------

The default language is english. French and german translations are provided. Please forgive my mistakes :-)
