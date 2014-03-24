# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import (
    add,
    list_all,
    delete,
    update,
    view
)


urlpatterns = patterns('',
                       url(r'^$', list_all, name='jobs_list_all'),
                       url(r'^add$', add, name='jobs_add'),
                       url(r'^edit/$', update),
                       url(r'^(?P<job_id>\d+)/$', view, name='jobs_view'),
                       url(r'^(?P<job_id>\d+)/delete$',
                           delete, name='jobs_delete'),
                       url(r'^(?P<job_id>\d+)/update$',
                           update, name='jobs_update'),
                       )
