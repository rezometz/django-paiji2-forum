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

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(
        r'^$',
        login_required(views.TopicListView.as_view()),
        name='topic-list',
    ),
    url(
        r'^recent/$',
        login_required(views.NewMessagesView.as_view()),
        name='recent-list',
    ),
    url(
        r'^unread/$',
        login_required(views.UnreadMessagesView.as_view()),
        name='unread',
    ),
    url(
        '^message/(?P<pk>[0-9]+)$',
        login_required(views.TopicView.as_view()),
        name='message',
    ),
    url(
        '^message/(?P<pk>[0-9]+)/answer$',
        login_required(views.AnswerCreate.as_view()),
        name='answer',
    ),
    url(
        '^new$',
        login_required(views.AnswerCreate.as_view()),
        name='new',
    ),
]
