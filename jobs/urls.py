from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.conf.urls import patterns, url
from .models import Job
from .views import JobCreate, JobList, JobDelete, JobUpdate, JobsFeed


urlpatterns = patterns('',
                       url(r'^$', JobList.as_view(), name='jobs_list_all'),
                       url(r'^rss$', JobsFeed(), name='jobs_feed'),
                       url(r'^add/$', login_required(
                           JobCreate.as_view()), name='jobs_add'),
                       url(r'^(?P<slug>[\w-]+)/$',
                           DetailView.as_view(model=Job),
                           name='jobs_view'),
                       url(r'^(?P<pk>\d+)/delete/$',
                           login_required(JobDelete.as_view()),
                           name='jobs_delete'),
                       url(r'^(?P<pk>\d+)/update/$',
                           login_required(JobUpdate.as_view()),
                           name='jobs_update'),
                       url(r'^tag/(?P<tag>[\w-]+)/$',
                           JobList.as_view(),
                           name='jobs_list_by_tag'),
                       )
