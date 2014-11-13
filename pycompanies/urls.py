# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.views.generic.detail import DetailView
from pycompanies.models import Company
from .views import (
    add,
    list_all,
    edit,
)


urlpatterns = patterns('',
    url(r'^$', list_all, name='companies_list_all'),
    url(r'^add$', add, name='companies-add'),
    url(r'^edit/$', edit),
    url(r'^(?P<company_id>\d+)/edit$', edit),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(model=Company),
        name='company_view'),
)
