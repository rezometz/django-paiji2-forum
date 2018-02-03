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
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView,\
    TemplateView, UpdateView
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin,\
    UserPassesTestMixin
from django.db.models import Count
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.db.models import Q
from .models import Message
from .forms import AnswerForm


TOPIC_NB = 20
MESSAGE_NB = 50


class TopicListView(ListView):

    template_name = 'forum/index.html'
    paginate_by = TOPIC_NB
    queryset = Message.objects\
        .root_nodes()\
        .order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        for msg in context['object_list']:
            msg.tree = msg.get_tree(
                user=self.request.user,
            )

        return context


class BurningTopicsView(ListView):

    template_name = 'forum/burning.html'
    paginate_by = TOPIC_NB

    def get_queryset(self):
        qs = Message.objects\
                .defer(
                    'text',
                    'author',
                    'icon',
                ).order_by(
                    '-pub_date',
                )
        m_list = list()
        tree_ids = set()
        for msg in qs.all():
            tree_id = msg.tree_id
            if tree_id not in tree_ids:
                msg.tree = msg.get_tree(
                    user=self.request.user,
                )
                tree_ids.add(tree_id)
                m_list += [msg]
        return m_list


class NewMessagesView(ListView):

    template_name = 'forum/recents.html'
    paginate_by = MESSAGE_NB

    def get_queryset(self):
        qs = Message.objects\
            .defer(
                 'text',
            ).order_by(
                '-pub_date',
            ).select_related(
                'author',
                'icon',
            ).annotate(
               readings=Count('readers'),
            )

        if self.request.user.is_authenticated():
            for i in qs:
                if not i.readers.filter(
                    pk=self.request.user.pk
                ).exists():
                    i.not_read = True

        return qs


class SearchMessagesView(NewMessagesView):

    def get_context_data(self, **kwargs):
        context =\
            super(SearchMessagesView, self).get_context_data(**kwargs)
        context.update({
            'q': self.request.GET.get('q', ''),
        })
        return context

    def get_queryset(self):
        qs = super(SearchMessagesView, self).get_queryset()
        if 'q' in self.request.GET:
            query = self.request.GET['q']
            words = query.split(' ')
            Qobj = Q()
            filtered = False
            for word in words:
                if word != '':
                    filtered = True
                    Qobj &= (
                        Q(text__icontains=word) |
                        Q(title__icontains=word) |
                        Q(author__username__icontains=word)
                    )
            if filtered:
                qs = qs.filter(Qobj)
        return qs


class UnreadMessagesView(LoginRequiredMixin, NewMessagesView):

    template_name = 'forum/unread.html'

    def get_queryset(self):
        qs = super(UnreadMessagesView, self).get_queryset()
        return qs.exclude(readers__pk=self.request.user.pk)


class ProfileMessagesView(NewMessagesView):

    template_name = 'forum/profile.html'
    paginate_by = MESSAGE_NB

    def get_queryset(self):
        qs = super(ProfileMessagesView, self).get_queryset()
        return qs.filter(author__pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProfileMessagesView, self).get_context_data(**kwargs)
        context.update({
            'author': get_object_or_404(
                get_user_model(),
                pk=self.kwargs['pk']
            ),
        })
        return context


class TopicView(TemplateView):

    template_name = 'forum/topic.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        message = get_object_or_404(
            Message,
            pk=self.kwargs['pk'],
        )

        user = self.request.user

        object_list = message.get_tree(
            user=user,
            text=True,
            read=True,
        )

        context.update({
            'prev_topic': message.prev_topic,
            'next_topic': message.next_topic,
            'object_list': object_list,
        })
        return context


class AnswerCreate(LoginRequiredMixin, CreateView):

    form_class = AnswerForm

    def get_template_names(self):
        if 'pk' in self.kwargs:
            return ['forum/topic.html']
        else:
            return ['forum/new.html']

    def get_context_data(self, **kwargs):
        context = super(AnswerCreate, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            message = get_object_or_404(
                Message,
                pk=self.kwargs['pk'],
            )
            object_list = message.get_tree(
                user=self.request.user,
                text=True,
                read=False,
            )
            context.update({
                'object_list': object_list,
            })
        return context

    def get_success_url(self):
        self.object.readers.add(self.request.user)
        self.object.save()
        return reverse(
            'forum:message',
            args=[self.object.pk],
        ) + "#forum-message"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pub_date = timezone.now()
        if 'pk' in self.kwargs:
            form.instance.question = get_object_or_404(
                Message,
                pk=self.kwargs['pk'],
             )
        else:
            form.instance.question = None
        return super(AnswerCreate, self).form_valid(form)


class AnswerUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Message
    form_class = AnswerForm
    template_name = 'forum/topic.html'
    raise_exception = True

    def test_func(self):
        message = get_object_or_404(
            Message,
            pk=self.kwargs['pk'],
        )
        return message.author == self.request.user

    permission_denied_message = _(
        'You are NOT authenticated as the author \
        of the message you want to update!'
    )

    def get_context_data(self, **kwargs):
        context = super(AnswerUpdate, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            message = get_object_or_404(
                Message,
                pk=self.kwargs['pk'],
            )
            object_list = message.get_tree(
                user=self.request.user,
                text=True,
                read=False,
            )
            context.update({
                'object_list': object_list,
                'update': True,
            })
        return context

    def get_success_url(self):
        self.object.readers.add(self.request.user)
        self.object.save()
        return reverse(
            'forum:message',
            args=[self.object.pk],
        ) + "#forum-message"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pub_date = timezone.now()
        return super(AnswerUpdate, self).form_valid(form)
