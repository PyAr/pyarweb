# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import (EventDetail,
                    EventList,
                    EventCreate,
                    EventUpdate,
                    EventDelete,
                    EventsFeed,
                    EventParticipationList,
                    EventParticipationCreate,
                    EventParticipationDetail,
                    EventParticipationDelete,
                    EventParticipationDownload)

urlpatterns = patterns(
    '',
    url(r'^$', EventList.as_view(), name='events_list_all'),
    url(r'^rss$', EventsFeed(), name='events_feed'),
    url(r'^(?P<pk>\d+)/$', EventDetail.as_view(), name='detail'),
    url(r'^add/$', EventCreate.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/editar/$', EventUpdate.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/borrar/$', EventDelete.as_view(), name='delete'),

    # Event Registration Management
    url(r'^(?P<pk>\d+)/inscribirse/$', EventParticipationCreate.as_view(), name='register'),
    url(r'^(?P<pk>\d+)/inscriptos/$', EventParticipationList.as_view(), name='registered'),
    url(r'^(?P<pk>\d+)/inscriptos/csv/$', EventParticipationDownload.as_view(),
        name='registered_csv'),
    url(r'^(?P<pk>\d+)/inscripcion/(?P<participation_pk>\d+)/$', EventParticipationDetail.as_view(),
        name='registration'),
    url(r'^(?P<pk>\d+)/inscripcion/(?P<participation_pk>\d+)/borrar/$',
        EventParticipationDelete.as_view(), name='unregister'),
)
