# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from django.views.generic.detail import DetailView
from pycompanies.models import Company
from .views import (
    add,
    list_all,
    edit,
    CompanyCreate,
    CompanyUpdate,
)


urlpatterns = patterns('',
    url(r'^$', list_all, name='companies_list_all'),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(model=Company),
        name='company_view'),
    url(r'^(?P<pk>\d+)/update/$',
        login_required(CompanyUpdate.as_view()),
        name='company_update'),
    url(r'^add/$',
        login_required(CompanyCreate.as_view()),
        name='company_create'),
)
