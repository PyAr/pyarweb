# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import (
    add,
    view,
    delete,
    update,
    list_all,
)


urlpatterns = patterns('',
    url(r'^$', list_all, name='projects_list_all'),
    url(r'^add$', add, name='projects_add'),
    url(r'^(?P<project_id>\d+)$', view, name='projects_view'),
    url(r'^(?P<project_id>\d+)/delete$', delete, name='projects_delete'),
    url(r'^(?P<project_id>\d+)/update$', update, name='projects_update'),
)
