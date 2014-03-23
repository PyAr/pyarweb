# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import (
    padawan_add,
    jedi_add,
    jedi_list,
    padawan_list,
    jedi_request,
)


urlpatterns = patterns('',

    url(r'^padawan/register$', padawan_add, name='padawan.add'),
    url(r'^jedi/register$', jedi_add, name='jedi.add'),

    url(r'^padawan/list$', padawan_list, name='padawan.list'),
    url(r'^jedi/list$', jedi_list, name='jedi.list'),

    url(r'^request/(?P<jedi_id>\d+)$', jedi_request, name='jedi.request')
)
