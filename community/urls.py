from django.urls import re_path
from django.conf.urls import patterns


urlpatterns = patterns(
    '',
    re_path(r'^', 'community.views.homepage', name='homepage'),
)
