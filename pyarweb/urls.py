# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from .views import (
    irc, special_page,
)

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', include('community.urls')),
    url(r'^irc/$', irc, name='irc'),
    url(r'^aprendiendo-python/$', special_page, {'slug': 'AprendiendoPython',
                                         'title': 'Aprendiendo Python'}, name='aprendiendo'),
    url(r'^sobre-pyar/$', special_page, {'slug': 'QuienesSomos',
                                  'title': 'Acerca de PyAr'}, name='about_pyar'),
    url(r'^miembros/$', special_page, {'slug': 'MiembrosDePyAr',
                                          'title': '¿Donde viven los miembros de PyAr?' }, name='pyar_members'),
    url(r'^lista/$', special_page, {'slug': 'ListaDeCorreob',
                        'title': 'Lista de correo'}, name='mailing_list'),
    url(r'^noticias/', include('news.urls')),
    url(r'^companies/', include('pycompanies.urls', namespace='companies')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^newbie/', include('newbie.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^faq/', include('faq.urls')),
    url(r'^planet/', include('planet.urls')),
    url(r'^wiki/', include('waliki.urls')),
)