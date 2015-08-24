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

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey


class MessageIcon(models.Model):

    class Meta:
        verbose_name = _('message icon')
        verbose_name_plural = _('message icons')

    name = models.CharField(max_length=30, verbose_name=_('name'))
    filename = models.CharField(max_length=100, verbose_name=_('filename'))

    def url(self):
        """return the icon's url"""
        # return settings.STATIC_URL + 'forum/icons/' + self.filename
        return 'forum/icons/' + self.filename

    def __unicode__(self):
        return self.name


class Message(MPTTModel):

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    class MPTTMeta:
        order_insertion_by = ['pub_date',]
        parent_attr = 'question'

    title = models.CharField(
        max_length=200,
        verbose_name=_('title'),
    )

    text = models.TextField(
        verbose_name=_('text'),
    )

    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('publication date'),
    )

    readers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='read_messages',
        verbose_name=_('readers'),
        blank=True,
    )

    question = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        verbose_name=_('question'),
        related_name='answers',
        db_index=True,
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        related_name='messages',
    )

    icon = models.ForeignKey(
        MessageIcon,
        default=None,
        verbose_name=_('icon'),
    )
    
    def topic(self):
        """return the current topic's first message"""
        return self.get_root()
    topic.short_description = _('current topic')

    def prev_topic(self):
        """return the previous topic's first message"""
        return self.topic().get_previous_sibling()
    prev_topic.short_description = _('previous topic')

    def next_topic(self):
        """return the next topic's first message"""
        return self.topic().get_next_sibling()
    next_topic.short_description = _('next topic')

    def get_tree(self):
        """return all the messages of the current topic, in tree order"""
        return self.topic().get_descendants(include_self=True)

    def is_topic(self):
        """return if the message is a topic's first message"""
        return self.is_root_node()
    is_topic.boolean = True
    is_topic.short_description = _('Is it a topic ?')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'forum:message',
            kwargs={'pk': self.pk},
        )
