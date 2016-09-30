# -*- coding: utf-8 -*-
# Copyright (C) 2016 Louis-Guillaume DUBOIS
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

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers, generics

from .models import Message, MessageIcon


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
        )


class MessageIconSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageIcon
        fields = (
            'filename',
        )


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'pk',
        )


class MessageSerializer(serializers.HyperlinkedModelSerializer):

    question = QuestionSerializer()

    icon = MessageIconSerializer()

    author = UserSerializer()

    title = serializers.CharField(
        min_length=3,
    )

    text = serializers.CharField(
        min_length=4,
        trim_whitespace=False,
    )

    class Meta:
        model = Message
        fields = (
            'pk',
            'question',
            'level',
            'is_burning',
            'is_new',
            'icon',
            'title',
            'pub_date',
            'author',
            'text',
        )
        depth = 1


class TopicSerializer(MessageSerializer):

    url = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='topic-detail',
    )

    class Meta:
        model = Message
        fields = (
            'pk',
            'url',
            'is_burning',
            'is_new',
            'icon',
            'title',
            'pub_date',
            'author',
        )
        depth = 1


class TopicList(generics.ListAPIView):

    serializer_class = TopicSerializer

    queryset = Message.objects\
        .root_nodes()\
        .order_by('-pub_date')


class TopicDetail(generics.ListAPIView):

    pagination_class = None

    serializer_class = MessageSerializer

    def get_queryset(self):
        message = get_object_or_404(
            Message, pk=self.kwargs['pk']
        )
        return message.get_tree(
            user=None,
            text=True,
            read=False,
        )
