# -*- coding: utf-8 -*-


"""URLS configurations for PyAr Web."""


from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from waliki.settings import WALIKI_SLUG_PATTERN

from .views import buscador, irc, old_url_redirect


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
    url(r'^aprendiendo-python/', 'community.views.learning', name='aprendiendo'),
    url(r'^nosotros/', 'community.views.about_pyar', name='about_pyar'),
    url(r'^miembros/', 'community.views.members', name='pyar_members'),
    url(r'^lista/', 'community.views.mailing_list', name='mailing_list'),

    url(r'^noticias/', include('news.urls')),
    url(r'^empresas/', include('pycompanies.urls', namespace='companies')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^trabajo/', include('jobs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^eventos/', include('events.urls', namespace='events')),
    # Descomentar cuando planet este funcionando
    # url(r'^planeta/', include('planet.urls')),
    # No se que va a pasar con la app de newbie, lanzamos primer release y
    # lo comento hasta que se decida que se hace
    # url(r'^newbie/', include('newbie.urls')),
    # No se que va a pasar con la app de project, lanzamos primer release y
    # lo comento hasta que se decida que se hace
    # url(r'^projects/', include('projects.urls')),
    # url(r'^faq/', include('faq.urls')),
    url(r'^wiki/', include('waliki.urls')),
    url(r'^(pyar/)?(?P<slug>' + WALIKI_SLUG_PATTERN + ')/?',
        old_url_redirect, name='old_url_redirect'),
)
