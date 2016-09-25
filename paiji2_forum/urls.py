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
