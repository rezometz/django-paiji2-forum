# -*- coding: utf-8 -*-
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

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from .models import Message, MessageIcon

User = get_user_model()


class MyTest(TestCase):

    def access(self, name, code):
        response = self.client.get(reverse(name))
        self.assertEqual(response.status_code, code)

    def access_url(self, url, code):
        response = self.client.get(url)
        self.assertEqual(response.status_code, code)

    def setUp(self):
        self.iseult = User.objects.create_user(
            username='iseult',
            email='iseult@te.st',
            password='iseult_password',
        )
        self.cesar = User.objects.create_user(
            username='cesar',
            email='cesar@te.st',
            password='cesar_password',
        )
        self.icon = MessageIcon.objects.create(
            name='test icon',
            filename='test_icon',
        )
        self.iseult_topic = Message.objects.create(
            title=u'test title ®®',
            text=u''' tstra auileæ~ǜß®\œù©þðĳþ’ù&æþiàn

                auieiiausrecpiu t'yx.lmmd
                =51476415678986451u4àuià,jl(è«épt,i.
                ''',
            question=None,
            author=self.iseult,
            icon=self.icon,
        )
        self.client = Client(enforce_csrf_checkts=True)


class ReadTestCase(MyTest):

    def test_authentication(self):

        # unauthenticated user
        self.access('forum:topic-list', 302)
        self.access('forum:recent-list', 302)
        self.access('forum:unread', 302)
        self.access('forum:new', 302)
        self.access_url(
            self.iseult_topic.get_absolute_url(),
            302,
        )
        self.access_url(
            reverse(
                'forum:message',
                kwargs={'pk': self.iseult_topic.pk},
            ),
            302,
        )
        self.access_url(
            reverse(
                'forum:answer',
                kwargs={'pk': self.iseult_topic.pk},
            ),
            302,
        )
        # nonexistant message
        self.access_url(
            reverse(
                'forum:message',
                kwargs={'pk': self.iseult_topic.pk + 1000},
            ),
            302,
        )
        self.access_url(
            reverse(
                'forum:answer',
                kwargs={'pk': self.iseult_topic.pk + 1000},
            ),
            302,
        )

        # authenticated user
        self.client.login(
            username='iseult',
            password='iseult_password',
        )
        self.access('forum:topic-list', 200)
        self.access('forum:recent-list', 200)
        self.access('forum:unread', 200)
        self.access('forum:new', 200)
        self.access_url(
            self.iseult_topic.get_absolute_url(),
            200,
        )
        self.access_url(
            reverse(
                'forum:message',
                kwargs={'pk': self.iseult_topic.pk},
            ),
            200,
        )
        self.access_url(
            reverse(
                'forum:answer',
                kwargs={'pk': self.iseult_topic.pk},
            ),
            200,
        )
        # nonexistant message
        self.access_url(
            reverse(
                'forum:message',
                kwargs={'pk': self.iseult_topic.pk + 1000},
            ),
            404,
        )
        self.access_url(
            reverse(
                'forum:answer',
                kwargs={'pk': self.iseult_topic.pk + 1000},
            ),
            404,
        )
