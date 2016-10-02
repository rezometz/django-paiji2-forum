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

from django.conf.urls import url

from . import views


app_name = 'forum'

urlpatterns = [
    url(
        r'^$',
        views.TopicListView.as_view(),
        name='topic-list',
    ),
    url(
        r'^burning/$',
        views.BurningTopicsView.as_view(),
        name='burning-list',
    ),
    url(
        r'^recent/$',
        views.NewMessagesView.as_view(),
        name='recent-list',
    ),
    url(
        r'^search/$',
        views.SearchMessagesView.as_view(),
        name='search-list',
    ),
    url(
        r'^unread/$',
        views.UnreadMessagesView.as_view(),
        name='unread',
    ),
    url(
        '^message/(?P<pk>[0-9]+)$',
        views.TopicView.as_view(),
        name='message',
    ),
    url(
        '^message/(?P<pk>[0-9]+)/answer/$',
        views.AnswerCreate.as_view(),
        name='answer',
    ),
    url(
        '^message/(?P<pk>[0-9]+)/update/$',
        views.AnswerUpdate.as_view(),
        name='update',
    ),
    url(
        '^new/$',
        views.AnswerCreate.as_view(),
        name='new',
    ),
    url(
        '^profile/(?P<pk>[0-9]+)$',
        views.ProfileMessagesView.as_view(),
        name='profile',
    ),
]
