from django.urls import re_path

from .views import (
  CompanyAdminView,
  CompanyAnalyticsView,
  CompanyAssociateView,
  CompanyAssociationListView,
  CompanyCreateView,
  CompanyDeleteView,
  CompanyDetailView,
  CompanyDisassociateView,
  CompanyListView,
  CompanyUpdateView
)

app_name = 'pycompanies'
urlpatterns = [
    re_path(r'^$', CompanyListView.as_view(), name='company_list_all'),
    re_path(r'^(?P<pk>\d+)/$', CompanyDetailView.as_view(), name='detail'),
    re_path(r'^agregar/$', CompanyCreateView.as_view(), name='add'),
    re_path(r'^(?P<pk>\d+)/editar/$', CompanyUpdateView.as_view(), name='edit'),
    re_path(r'^(?P<pk>\d+)/eliminar/$', CompanyDeleteView.as_view(), name='delete'),
    re_path(r'^(?P<company>\d+)/asociar/$', CompanyAssociateView.as_view(), name='associate'),
    re_path(r'^asociarme/$', CompanyAssociationListView.as_view(), name='association_list'),
    re_path(r'^admin/$', CompanyAdminView.as_view(), name='admin'),
    re_path(r'^(?P<pk>\d+)/desasociar/$', CompanyDisassociateView.as_view(), name='disassociate'),
    re_path(r'^(?P<pk>\d+)/analitica/$', CompanyAnalyticsView.as_view(), name='analytics')
]
