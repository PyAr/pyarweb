# -*- coding: utf-8 -*-


"""URLS configurations for PyAr Web."""
import re

from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path
from django.views.static import serve

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

    # no puedo usar el static porque no funcia en produccion y en prod django esta
    # sirviendo los archivos estaticos. Esto es sacado del codigo de la funcion.
    # si es un HACK, pero hasta que pueda solucionarlo usando django-assets o algo asi
    re_path(
        r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')),
        serve,
        kwargs=dict(document_root=settings.STATIC_ROOT)
    ),
    re_path(
        r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
        serve,
        kwargs=dict(document_root=settings.MEDIA_ROOT)
    ),
]
