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

from django.test import TestCase
from django.utils import timezone
from htmlvalidator.client import ValidatingClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import timedelta
from models import Message, MessageIcon
from update_db import update_icons_db


User = get_user_model()


class UpdateDBTest(TestCase):

    def setUp(self):
        self.client = ValidatingClient()

    def test_update_db(self):
        update_icons_db()
        icon0 = MessageIcon.objects.get(name="1a.gif")
        icon1 = MessageIcon.objects.get(name="union-jack.png")
        self.assertFalse(icon0 == icon1)


class MyTest(TestCase):

    def path(self, url):
        return url
        # return '/' + '/'.join(url.split('/')[3:])

    def setUp(self):
        update_icons_db()
        self.icon = MessageIcon.objects.get(name="photo.gif")
        self.icon0 = MessageIcon.objects.get(name="1a.gif")
        self.icon1 = MessageIcon.objects.get(name="union-jack.png")
        self.client = ValidatingClient()
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

        self._post_first_message()

    def access(self, name, code):
        response = self.client.get(reverse(name))
        self.assertEqual(response.status_code, code)

    def access_url(self, url, code):
        response = self.client.get(url)
        self.assertEqual(response.status_code, code)

    def _post_first_message(self):
        self.client.login(
            username='iseult',
            password='iseult_password',
        )
        response = self.client.post(
            reverse('forum:new'),
            {
                'icon': self.icon.pk,
                'title': u'test title ®®',
                'text': u''' tstra auileæ~ǜß®\œù©þðĳþ’ù&æþiàn

                auieiiausrecpiu t'yx.lmmd
                =51476415678986451u4àuià,jl(è«épt,i.
                ''',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.first_message = Message.objects.get(title=u'test title ®®')
        self.assertEqual(
            self.path(response['Location']),
            self.first_message.get_absolute_url(),
        )
        self.assertEqual(
            self.path(response['Location']),
            reverse(
                'forum:message',
                args=[self.first_message.pk]
            ) + '#forum-message',
        )
        self.access_url(self.first_message.get_absolute_url(), 200)
        self.client.logout()


class NameTestCase(MyTest):

    def test_name(self):
        self.assertEqual(
            self.first_message.__unicode__(),
            unicode(self.first_message.title),
        )


class AccessTestCase(MyTest):

    def test_unauthenticated_user(self):

        self.access('forum:topic-list', 200)
        self.access('forum:burning-list', 200)
        self.access('forum:unread', 302)
        self.access('forum:new', 302)
        self.access_url(
            self.first_message.get_absolute_url(),
            200,
        )
        self.access_url(
            reverse(
                'forum:message',
                kwargs={'pk': self.first_message.pk},
            ),
            200,
        )
        self.access_url(
            reverse(
                'forum:answer',
                kwargs={'pk': self.first_message.pk},
            ),
            302,
        )
        self.access_url(
            reverse(
                'forum:profile',
                kwargs={'pk': self.iseult.pk},
            ),
            200,
        )
        # nonexistant message
        self.access_url(
            reverse(
                'forum:message',
                kwargs={'pk': self.first_message.pk + 1000},
            ),
            404,
        )
        self.access_url(
            reverse(
                'forum:answer',
                kwargs={'pk': self.first_message.pk + 1000},
            ),
            302,
        )
        self.access_url(
            reverse(
                'forum:profile',
                kwargs={'pk': self.iseult.pk + 1000},
            ),
            404,
        )

    def test_authenticated_user(self):

        self.client.login(
            username='iseult',
            password='iseult_password',
        )
        self.access('forum:topic-list', 200)
        self.access('forum:burning-list', 200)
        self.access('forum:unread', 200)
        self.access('forum:new', 200)
        self.access_url(
            self.first_message.get_absolute_url(),
            200,
        )
        self.access_url(
            reverse(
                'forum:message',
                kwargs={'pk': self.first_message.pk},
            ),
            200,
        )
        self.access_url(
            reverse(
                'forum:answer',
                kwargs={'pk': self.first_message.pk},
            ),
            200,
        )
        self.access_url(
            reverse(
                'forum:profile',
                kwargs={'pk': self.iseult.pk},
            ),
            200,
        )
        # nonexistant message
        self.access_url(
            reverse(
                'forum:message',
                kwargs={'pk': self.first_message.pk + 1000},
            ),
            404,
        )
        self.access_url(
            reverse(
                'forum:answer',
                kwargs={'pk': self.first_message.pk + 1000},
            ),
            404,
        )
        self.access_url(
            reverse(
                'forum:profile',
                kwargs={'pk': self.iseult.pk + 1000},
            ),
            404,
        )


class DateTestCase(MyTest):

    def test_is_new(self):

        self.assertEqual(
            self.first_message.is_new(),
            True,
        )

        self.assertEqual(
            self.first_message.is_burning(),
            True,
        )

        hours = 24
        delta = timedelta(hours=hours)

        old_message = Message.objects.create(
            title='my old message',
            text="""My old text""",
            pub_date=timezone.now() - delta - timedelta(hours=2),
            author=self.iseult,
            question=self.first_message,
            icon=self.icon,
        )

        self.assertEqual(
            old_message.is_new(hours),
            False,
        )

        self.assertEqual(
            old_message.is_burning(hours),
            False,
        )


class CreationTestCase(MyTest):

    def test_creation(self):

        # new topic

        self.client.login(
            username='iseult',
            password='iseult_password',
        )

        self.access('forum:topic-list', 200)

        self.access('forum:new', 200)

        response = self.client.post(
            reverse('forum:new'),
            {
                'icon': self.icon.pk,
                'title': 'an other topic',
                'text': """Hello ! I hope you
                            spend good holidays !""",
            }
        )

        self.assertEqual(response.status_code, 302)

        message = Message.objects.get(title='an other topic')

        self.assertEqual(
            self.path(response['Location']),
            message.get_absolute_url(),
        )
        self.access_url(response['Location'], 200)

        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(message.author, self.iseult)
        self.assertEqual(set(message.readers.all()), set((self.iseult,)))
        self.assertEqual(message.icon, self.icon)
        self.assertEqual(message.question, None)
        self.assertEqual(message.topic(), message)
        self.assertEqual(message.prev_topic(), self.first_message)
        self.assertEqual(message.next_topic(), None)
        self.assertEqual(message.is_topic(), True)
        self.access_url(message.get_absolute_url(), 200)

        # last topic

        self.client.login(
            username='cesar',
            password='cesar_password',
        )

        self.access('forum:new', 200)

        icon = self.icon1
        title = u'last topic'
        text = u"""Hi ! How do you do ?"""
        response = self.client.post(
            reverse('forum:new'),
            {
                'icon': icon.pk,
                'title': title,
                'text': text,
            }
        )

        self.assertEqual(response.status_code, 302)

        last_message = Message.objects.get(title='last topic')
        self.assertEqual(
            last_message.icon,
            icon
        )
        self.assertEqual(
            last_message.title,
            title
        )
        self.assertEqual(
            last_message.text,
            text
        )

        self.assertEqual(
            self.path(response['Location']),
            last_message.get_absolute_url(),
        )
        self.access_url(response['Location'], 200)

        self.assertEqual(Message.objects.count(), 3)
        self.assertEqual(last_message.author, self.cesar)
        self.assertEqual(set(last_message.readers.all()), set((self.cesar,)))
        self.assertEqual(last_message.question, None)
        self.assertEqual(last_message.topic(), last_message)
        self.assertEqual(last_message.prev_topic(), message)
        self.assertEqual(last_message.next_topic(), None)
        self.assertEqual(last_message.is_topic(), True)
        self.access_url(last_message.get_absolute_url(), 200)

        # how did it change the other topics ?

        self.assertEqual(message.author, self.iseult)
        self.assertEqual(set(message.readers.all()), set((self.iseult,)))
        self.assertEqual(message.icon, self.icon)
        self.assertEqual(message.question, None)
        self.assertEqual(message.topic(), message)
        self.assertEqual(message.prev_topic(), self.first_message)
        self.assertEqual(message.next_topic(), last_message)
        self.assertEqual(message.is_topic(), True)
        self.access_url(message.get_absolute_url(), 200)


class UpdateTestCase(MyTest):

    def _test_denied_update(self):
        read_url = self.first_message.get_absolute_url()
        self.access_url(read_url, 200)
        update_url = reverse(
            'forum:update',
            kwargs={'pk': self.first_message.pk}
        )
        get_response = self.client.get(update_url)
        self.assertEqual(get_response.status_code, 403)
        old_title = self.first_message.title
        old_text = self.first_message.text
        title = u'my braund new title -_- ^^'
        text = u'''hello this is our new
                    message ^^

                    æùßþ»/«(bètuidà'''
        post_response = self.client.post(
            update_url,
            {
                'icon': self.icon0.pk,
                'text': text,
                'title': title,
            }
        )
        self.assertEqual(
            post_response.status_code,
            403
        )
        self.assertEqual(
            self.first_message.title,
            old_title
        )
        self.assertEqual(
            unicode(self.first_message.text),
            unicode(old_text)
        )
        self.assertEqual(
            self.first_message.icon.pk,
            self.icon.pk
        )

    def test_anonymous_update(self):
        self._test_denied_update()

    def test_logged_reader_update(self):
        self.client.login(
            username='cesar',
            password='cesar_password',
        )
        self._test_denied_update()
        self.client.logout()

    def test_author_update(self):
        self.client.login(
            username='iseult',
            password='iseult_password',
        )
        update_url = reverse(
            'forum:update',
            kwargs={'pk': self.first_message.pk}
        )
        self.access_url(update_url, 200)
        title = u'new title :-) ®®æù>÷|'
        text = u'''plop this is my new
                    message ^^

                    æùßþ»/«(bètuidà'''
        post_response = self.client.post(
            update_url,
            {
                'icon': self.icon1.pk,
                'title': title,
                'text': text,
            }
        )
        self.assertEqual(post_response.status_code, 302)
        message = Message.objects.get(title=title)
        self.assertEqual(
            message.pk,
            self.first_message.pk
        )
        self.assertEqual(
            message.icon.pk,
            self.icon1.pk
        )
        self.assertEqual(
            message.title,
            title
        )
        self.assertEqual(
            unicode(message.text),
            unicode(text)
        )
        self.assertEqual(
            self.path(post_response['Location']),
            self.first_message.get_absolute_url()
        )
        self.assertEqual(
            self.path(post_response['Location']),
            reverse(
                'forum:message',
                args=[self.first_message.pk]
            ) + '#forum-message',
        )
        self.access_url(self.first_message.get_absolute_url(), 200)
        self.client.logout()


class ReadersTestCase(MyTest):

    def test_readers(self):

        self.client.login(
            username='cesar',
            password='cesar_password',
        )

        # new topic
        response = self.client.post(
            reverse('forum:new'),
            {
                'icon': self.icon.pk,
                'title': 'topic of cesar',
                'text': """Hi ! How do you do ? """,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.second_message = Message.objects.get(title='topic of cesar')

        self.assertEqual(
            set(self.second_message.readers.all()),
            set((self.cesar,)),
        )

        self.assertEqual(
            set(self.first_message.readers.all()),
            set((self.iseult,)),
        )

        # cesar visits the first topic

        self.access_url(self.first_message.get_absolute_url(), 200)

        # how does it change the "readers" values ?
        self.assertEqual(
            set(self.first_message.readers.all()),
            set((self.iseult, self.cesar)),
        )
        self.assertEqual(
            set(self.second_message.readers.all()),
            set((self.cesar,)),
        )

        # cesar answers the first topic

        response = self.client.post(
            reverse('forum:answer', args=[self.first_message.pk]),
            {
                'icon': self.icon.pk,
                'title': 'answer',
                'text': 'everything is in the title',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.answer = Message.objects.order_by('-pub_date').all()[0]
        self.assertEqual(
            self.path(response['Location']),
            self.answer.get_absolute_url(),
        )
        self.access_url(self.answer.get_absolute_url(), 200)

        # iseult visits the second message

        self.client.login(
            username='iseult',
            password='iseult_password',
        )
        self.access_url(self.second_message.get_absolute_url(), 200)

        # how does it change the "readers" values ?
        self.assertEqual(
            set(self.first_message.readers.all()),
            set((self.iseult, self.cesar)),
        )
        self.assertEqual(
            set(self.answer.readers.all()),
            set((self.cesar,)),
        )
        self.assertEqual(
            set(self.second_message.readers.all()),
            set((self.cesar, self.iseult)),
        )

        # iseult visits the first message
        self.access_url(self.first_message.get_absolute_url(), 200)

        # how does it change the "readers" values ?
        self.assertEqual(
            set(self.first_message.readers.all()),
            set((self.iseult, self.cesar)),
        )
        self.assertEqual(
            set(self.answer.readers.all()),
            set((self.cesar, self.iseult)),
        )
        self.assertEqual(
            set(self.second_message.readers.all()),
            set((self.cesar, self.iseult)),
        )
