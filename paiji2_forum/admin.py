# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Louis-Guillaume DUBOIS
#
# This file is part of paiji2-forum
#
# paiji2-forum is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# paiji2-forum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from mptt.admin import MPTTModelAdmin
from .models import Message
from .forms import Markdownarea


class MessageAdmin(MPTTModelAdmin):

    list_display = (
        'title', 'author', 'pub_date',
        'icon', 'is_topic', 'topic',
        'is_new', 'is_burning'
    )

    list_filter = ('pub_date', 'author')

    search_fields = ['title', 'text', 'author__username']

    formfield_overrides = {
        models.TextField: {
            'strip': False,
            'widget': Markdownarea,
        },
    }

    class Media:
        css = {
            'all': ('forum/style.css',),
        }
        js = (
            'forum/markdown.js',
            'forum/editor.js',
        )


admin.site.register(Message, MessageAdmin)
