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
from django.utils.translation import ugettext as _
from django.forms import ModelForm, RadioSelect,\
    ModelChoiceField, TextInput, CharField, Textarea
# from django.utils.encoding import force_text
# from django.utils.html import format_html
# from django.forms.utils import flatatt
from .models import Message, MessageIcon


class IconField(ModelChoiceField):

    def label_from_instance(self, obj):
        # return '<img class="icon" src="'+obj.url()+'" alt="'+obj.name+'"/>'
        return obj.url()


class Markdownarea(Textarea):
    pass


class AnswerForm(ModelForm):

    text = CharField(
        initial=_('''\
Use the *Markdown* format here.

Cf. [documentation](http://daringfireball.net/projects/markdown/basics).'''),
        widget=Markdownarea,
        strip=False,
        min_length=5,
    )
    title = CharField(
        widget=TextInput,
        strip=True,
        min_length=3,
    )
    try:
        icon = IconField(
            queryset=MessageIcon.objects.all(),
            initial=MessageIcon.objects.get(name='neutre.gif'),
            empty_label=None,
            widget=RadioSelect,
        )
    except Exception as e:
        icon = IconField(
            queryset=MessageIcon.objects.all(),
            initial=None,
            empty_label=None,
            widget=RadioSelect,
        )

    class Meta:
        model = Message
        fields = ['icon', 'title', 'text']
