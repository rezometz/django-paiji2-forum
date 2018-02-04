paiji2-forum
============


[![Build Status](https://travis-ci.org/rezometz/django-paiji2-forum.svg?branch=master)](https://travis-ci.org/rezometz/django-paiji2-forum)
[![Code Climate](https://codeclimate.com/github/rezometz/django-paiji2-forum/badges/gpa.svg)](https://codeclimate.com/github/rezometz/django-paiji2-forum)
[![Coverage Status](https://coveralls.io/repos/rezometz/django-paiji2-forum/badge.svg?branch=master&service=github)](https://coveralls.io/github/rezometz/django-paiji2-forum?branch=master)

Licenses
-------

- __paiji2-forum__: AGPLv3 [![Affero GPL v3](http://www.gnu.org/graphics/agplv3-88x31.png)](http://www.gnu.org/licenses/agpl-3.0.html) license

- __markdown.js__:  MIT license, comes from [evilstreak/markdown-js](https://github.com/evilstreak/markdown-js)

- __bootstrap__: MIT license, comes from [twbs/bootstrap](https://github.com/twbs/bootstrap)

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

`Django>=1.11` (including Django 2)

You must also install `django-bootstrap3` and `django-mptt` (pip will do this for you).
`django-html-validator` is required for testing purposes.

Installation
------------

### Installed apps

In the `settings.py` file of your project, add the following apps:

```python
INSTALLED_APPS = [
    # other apps…
    'paiji2_forum.apps.Paiji2ForumConfig',
    'mptt',
    'bootstrap3',
    # other apps…
]
```

### URLconf

Include `'paiji2_forum.urls'` in the `urlpatterns` of your project.
For instance:

```python
from django.conf.urls import url, include

urlpatterns = [
    # other urls…
    url(r'^forum/', include('paiji2_forum.urls')),
]
```

### Templates

See `paiji2_forum/templates/forum/base.html` for an example.

You should change the name of the extended template (line 1) to fit to your project.

The extended template should have a `title` block, a `style` block to add a css file link, and a `content` block to show the content of the forum.

It must also link to `bootstrap.css` or `bootstrap.min.css` (bootstrap version 3), for instance with:

```
<link rel="stylesheet" href="https://unpkg.com/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
```

Translations
------------

The default language is english. French and german translations are provided. Please forgive my mistakes :-)
