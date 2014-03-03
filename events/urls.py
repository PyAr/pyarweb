# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import (
	EventDetail,
	EventList,
	EventCreate,
	EventUpdate,
	EventDelete    
)


urlpatterns = patterns('',
    url(r'^$', EventList.as_view(), name='events_list_all'),
    url(r'^(?P<pk>\d+)/$', EventDetail.as_view(), name='detail'),
    url(r'^add/$', EventCreate.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/edit/$', EventUpdate.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', EventDelete.as_view(), name='delete'),
)
