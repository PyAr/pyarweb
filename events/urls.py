
from django.urls import re_path
from django.views.generic.detail import DetailView

from .models import Event
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

urlpatterns = [
    re_path(r'^$', EventList.as_view(), name='events_list_all'),
    re_path(r'^rss$', EventsFeed(), name='events_feed'),
    re_path(r'^(?P<pk>\d+)/$', EventDetail.as_view(), name='detail'),
    re_path(r'^add/$', EventCreate.as_view(), name='add'),
    re_path(r'^(?P<pk>\d+)/editar/$', EventUpdate.as_view(), name='edit'),
    re_path(r'^(?P<pk>\d+)/borrar/$', EventDelete.as_view(), name='delete'),
    re_path(r'^(?P<slug>[\w-]+)/$', DetailView.as_view(model=Event), name='event_slug'),

    # Event Registration Management
    re_path(r'^(?P<pk>\d+)/inscribirse/$', EventParticipationCreate.as_view(), name='register'),
    re_path(r'^(?P<pk>\d+)/inscriptos/$', EventParticipationList.as_view(), name='registered'),
    re_path(r'^(?P<pk>\d+)/inscriptos/csv/$', EventParticipationDownload.as_view(),
            name='registered_csv'),
    re_path(r'^(?P<pk>\d+)/inscripcion/(?P<participation_pk>\d+)/$',
            EventParticipationDetail.as_view(),
            name='registration'),
    re_path(r'^(?P<pk>\d+)/inscripcion/(?P<participation_pk>\d+)/borrar/$',
            EventParticipationDelete.as_view(), name='unregister'),
]
