# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import (
    add,
    list_all,
    edit,
)


urlpatterns = patterns('',
    url(r'^$', list_all, name='companies_list_all'),
    url(r'^/add$', add),
    url(r'^/edit/$', edit),
    url(r'^/(?P<company_id>\d+)/edit$', edit),
)
