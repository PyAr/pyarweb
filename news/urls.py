# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import (
    add,
    latest
)


urlpatterns = patterns('',
    url(r'^/latest$', latest),
    url(r'^/add$', add),
)
