# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import (
    add_padawan,
    add_jedi,
    list_padawan,
    list_jedi,
)


urlpatterns = patterns('',

    url(r'^padawan/register$', add_padawan, name='padawan.add'),
    url(r'^jedi/register$', add_jedi, name='jedi.add'),

    url(r'^padawan/list$', list_padawan, name='padawan.list'),
    url(r'^jedi/list$', list_jedi, name='jedi.list'),
)
