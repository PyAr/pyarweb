# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import (
    add,
    delete,
    update,
    list_all,
)


urlpatterns = patterns('',
    url(r'^$', list_all, name='news_list_all'),
    url(r'^/add$', add, name='news_add'),
    url(r'^/(?P<new_id>\d+)/delete$', delete, name='news_delete'),
    url(r'^/(?P<new_id>\d+)/update$', update, name='news_update'),
)
