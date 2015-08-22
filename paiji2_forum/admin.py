# Copyright (C) 2015 Louis-Guillaume DUBOIS
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

from django.contrib import admin
from .models import Message, MessageIcon


class AnswersInline(admin.TabularInline):
    model = Message
    extra = 0


class MessageAdmin(admin.ModelAdmin):
    inlines = [AnswersInline]
    list_display = (
        'title',
        'icon',
        'author',
        'pub_date',
        'is_topic',
        'topic',
        'level',
        'question',
        'is_leaf',
        'answers_nb',
        'childs_nb',
        'childs_depth',
        'text',
    )
    list_filter = ['pub_date', 'author']
    search_fields = ['title', 'text', 'author']


class MessageIconAdmin(admin.ModelAdmin):
    list_display = ('name', 'filename', 'url')
    search_fields = ['name', 'filename']

admin.site.register(Message, MessageAdmin)
admin.site.register(MessageIcon, MessageIconAdmin)
