from django.conf.urls import patterns, url
from .views import update_profile

urlpatterns = patterns('',
   url(r'^$', update_profile,
       name='update'),
)
