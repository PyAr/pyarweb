# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import (
    list_all,
)

urlpatterns = patterns('', url(r'^$', list_all, name='faq_all'),)
