# -*- coding: utf-8 -*-


"""URLS configurations for PyAr Web."""

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path

from .views import buscador, irc

from community.views import homepage

admin.autodiscover()

app_name = 'pyarweb'
urlpatterns = [
    re_path(r'^irc/$', irc, name='irc'),
    re_path(r'^buscador/$', buscador, name='buscador'),

    re_path(r'^$', homepage, name='homepage'),

    re_path(r'^noticias/', include('news.urls')),
    re_path(r'^empresas/', include(('pycompanies.urls', 'pycompanies'), namespace='companies')),
    re_path(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    re_path(r'^summernote/', include('django_summernote.urls')),
    re_path(r'^trabajo/', include('jobs.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^eventos/', include(('events.urls', 'events'), namespace='events')),
    re_path(r'^planeta/', include('planet.urls')),
    re_path(r'^captcha/', include('captcha.urls')),
    re_path(r'^email_confirmation/', include(('email_confirm_la.urls', 'email_confirm_la.urls'),
                                             namespace='email_confirm_la')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
