"""URLS configurations for PyAr Web."""
import re

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.urls import re_path
from django.views.static import serve

from .views import buscador, irc

from community.views import homepage

admin.autodiscover()

app_name = 'pyarweb'
urlpatterns = [
    path('irc/', irc, name='irc'),
    path('buscador/', buscador, name='buscador'),

    path('', homepage, name='homepage'),

    path('noticias/', include('news.urls')),
    path('empresas/', include(('pycompanies.urls', 'pycompanies'), namespace='companies')),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path('summernote/', include('django_summernote.urls')),
    re_path(r'^admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('eventos/', include(('events.urls', 'events'), namespace='events')),
    path('captcha/', include('captcha.urls')),
    path('trabajo/', include(('joboffers.urls', 'joboffers'), namespace='joboffers')),

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
