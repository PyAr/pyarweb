from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.urls import re_path
from .models import Job
from .views import (JobCreate, JobList, JobDelete, JobUpdate, JobsFeed,
                    JobInactivate)


urlpatterns = [
    re_path(r'^$', JobList.as_view(), name='jobs_list_all'),
    re_path(r'^rss$', JobsFeed(), name='jobs_feed'),
    re_path(r'^add/$', login_required(JobCreate.as_view()), name='jobs_add'),
    re_path(r'^(?P<slug>[\w-]+)/$', DetailView.as_view(model=Job), name='jobs_view'),
    re_path(r'^(?P<pk>\d+)/delete/$', login_required(JobDelete.as_view()), name='jobs_delete'),
    re_path(r'^(?P<pk>\d+)/update/$', login_required(JobUpdate.as_view()), name='jobs_update'),
    re_path(r'^(?P<pk>\d+)/inactivate/$', login_required(JobInactivate.as_view()),
            name='jobs_inactivate'),
]
