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


class MessageIcon(models.Model):

    class Meta:
        verbose_name = _('message icon')
        verbose_name_plural = _('message icons')

    name = models.CharField(max_length=30, verbose_name=_('name'))
    filename = models.CharField(max_length=100, verbose_name=_('filename'))

    def url(self):
        # return settings.STATIC_URL + 'forum/icons/' + self.filename
        return 'forum/icons/' + self.filename

    def __unicode__(self):
        return self.name


class Message(models.Model):

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')

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

    question = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        verbose_name=_('question'),
        related_name='answers',
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

    def is_topic(self):
        return self.question is None
    is_topic.boolean = True
    is_topic.short_description = _('Is it a topic?')

    def is_leaf(self):
        return self.answers.count() == 0
    is_leaf.boolean = True
    is_leaf.short_description = _('Does it have answers?')

    def answers_nb(self):
        return self.answers.count()
    answers_nb.short_description = _('number of answers')

    def childs_nb(self):
        nb = 0
        for answer in self.answers.all():
            nb += answer.childs_nb()
        return nb + self.answers.count()
    childs_nb.short_description = _(
        'number of answers and answers answers (recursive)'
        )

    def childs_depth(self):
        if self.answers.count() == 0:
            return 0
        else:
            return 1 + max(
                [i.childs_depth() for i in self.answers.all()]
            )

    def level(self):
        if self.question is None:
            return 0
        else:
            return 1 + self.question.level()
    level.short_description = _('depth level in the topic')

    def topic(self):
        if self.question is None:
            return self
        else:
            return self.question.topic()
    topic.short_description = _('topic of the message')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:message', kwargs={'pk': self.pk})
