# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import (
    padawan_add,
    jedi_add,
    jedi_list,
    padawan_list,
    jedi_request,
    register,
    jedi_answer,
)


urlpatterns = patterns('',

    url(r'^register$', register, name='register'),
    url(r'^padawan/register$', padawan_add, name='padawan.add'),
    url(r'^jedi/register$', jedi_add, name='jedi.add'),

    url(r'^padawan/list$', padawan_list, name='padawan.list'),
    url(r'^jedi/list$', jedi_list, name='jedi.list'),

    url(r'^request/(?P<jedi_id>\d+)$', jedi_request, name='jedi.request'),
    url(
        r'^send-answer/(?P<jedi_id>\d+)/(?P<padawan_id>\d+)/(?P<answer>.*)$',
        jedi_answer,
        name='jedi.answer'
    )
)
