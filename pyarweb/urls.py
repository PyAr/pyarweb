# -*- coding: utf-8 -*-


"""URLS configurations for PyAr Web."""


from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin

from .views import buscador, irc


admin.autodiscover()

urlpatterns = patterns(
    '',
    # Static files
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    # Media files
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

    url(r'^irc/$', irc, name='irc'),
    url(r'^buscador/$', buscador, name='buscador'),

    url(r'^$', 'community.views.homepage', name='homepage'),

    url(r'^noticias/', include('news.urls')),
    url(r'^empresas/', include('pycompanies.urls', namespace='companies')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^trabajo/', include('jobs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^eventos/', include('events.urls', namespace='events')),
    url(r'^planeta/', include('planet.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^email_confirmation/', include('email_confirm_la.urls',
                                         namespace='email_confirm_la')),
)
