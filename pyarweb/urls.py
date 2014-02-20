# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('community.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
