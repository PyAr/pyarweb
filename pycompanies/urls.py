from django.urls import re_path

from .views import (
    CompanyAdminView,
    CompanyAssociateView,
    CompanyAssociationListView,
    CompanyDetailView,
    CompanyListView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView,
    CompanyDisassociateView)

app_name = 'pycompanies'
urlpatterns = [
    re_path(r'^$', CompanyListView.as_view(), name='company_list_all'),
    re_path(r'^(?P<pk>\d+)/$', CompanyDetailView.as_view(), name='detail'),
    re_path(r'^add/$', CompanyCreateView.as_view(), name='add'),
    re_path(r'^(?P<pk>\d+)/edit/$', CompanyUpdateView.as_view(), name='edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', CompanyDeleteView.as_view(), name='delete'),
    re_path(r'^(?P<company>\d+)/associate/$', CompanyAssociateView.as_view(), name='associate'),
    re_path(r'^asociarme/$', CompanyAssociationListView.as_view(), name='association_list'),
    re_path(r'^admin/$', CompanyAdminView.as_view(), name='admin'),
    re_path(r'^(?P<pk>\d+)/disassociate/$',
            CompanyDisassociateView.as_view(), name='disassociate')
]
