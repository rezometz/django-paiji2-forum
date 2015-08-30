# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('text', models.TextField(verbose_name='text')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publication date')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('author', models.ForeignKey(related_name='messages', verbose_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
            },
        ),
        migrations.CreateModel(
            name='MessageIcon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('filename', models.CharField(max_length=100, verbose_name='filename')),
            ],
            options={
                'verbose_name': 'message icon',
                'verbose_name_plural': 'message icons',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='icon',
            field=models.ForeignKey(default=None, verbose_name='icon', to='paiji2_forum.MessageIcon'),
        ),
        migrations.AddField(
            model_name='message',
            name='question',
            field=mptt.fields.TreeForeignKey(related_name='answers', verbose_name='question', blank=True, to='paiji2_forum.Message', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='readers',
            field=models.ManyToManyField(related_name='read_messages', verbose_name='readers', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
