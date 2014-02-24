# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import (
    add,
    list_all,
)


urlpatterns = patterns('',
    url(r'^$', list_all, name='news_list_all'),
    url(r'^/add$', add),
)
