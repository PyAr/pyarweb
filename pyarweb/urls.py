# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from .views import (
    irc,
    QuienesSomos,
    MiembrosDePyAr,
    ListaDeCorreo
)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('community.urls')),
    url(r'^irc/', irc, name='irc'),
    url(r'^aboutpyar/', QuienesSomos, name='about_pyar'),
    url(r'^members/', MiembrosDePyAr, name='pyar_members'),
    url(r'^maillinglist/', ListaDeCorreo, name='mailling_list'),
    url(r'^news/', include('news.urls')),
    url(r'^companies/', include('pycompanies.urls')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^newbie/', include('newbie.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pyarenses/', include('registration.backends.default.urls')),
    url(r'^events/', include('events.urls', namespace='events')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
