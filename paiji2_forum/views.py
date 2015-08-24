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

# from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
# from django.http import Http404
from django.views.generic import ListView, CreateView,\
    TemplateView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Message, MessageIcon
from django.forms import ModelForm, RadioSelect,\
    ModelChoiceField, TextInput, Textarea


class TopicListView(ListView):

    template_name = 'forum/index.html'
    paginate_by = 12
    queryset = Message.objects.root_nodes().order_by('-pub_date')


class NewMessagesView(ListView):

    template_name = 'forum/recents.html'
    paginate_by = 30
    queryset = Message.objects.order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        return context


class UnreadMessagesView(NewMessagesView):

    template_name = 'forum/unread.html'
    paginate_by = 30

    def get_queryset(self):
        return Message.objects\
            .exclude(
                readers__pk=self.request.user.pk
            ).order_by(
                '-pub_date'
            )


class TopicView(TemplateView):

    template_name = 'forum/topic.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        message = get_object_or_404(
            Message,
            pk=self.kwargs['pk'],
        )
        object_list = message.topic().get_tree()
        context.update({
            'object_list': object_list,
            'message': message,
        })
        for msg in context['object_list']:
            if self.request.user not in msg.readers.all():
                msg.readers.add(self.request.user)
                msg.not_read = True  # to show the label...
        return context


class IconField(ModelChoiceField):

    def label_from_instance(self, obj):
        # return '<img class="icon" src="'+obj.url()+'" alt="'+obj.name+'"/>'
        return obj.url()


class AnswerForm(ModelForm):

    icon = IconField(
        queryset=MessageIcon.objects.all(),
        empty_label=None,
        widget=RadioSelect,
    )

    class Meta:
        model = Message
        fields = ['icon', 'title', 'text']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'text': Textarea(attrs={'class': 'form-control'}),
        }


class AnswerCreate(CreateView):

    form_class = AnswerForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnswerCreate, self).dispatch(*args, **kwargs)

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
            object_list = message.topic().get_tree()
            context.update({
                'object_list': object_list,
                'message': message,
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
