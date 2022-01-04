from django.urls import re_path

from .views import (
    CompanyAdmin,
    CompanyAssociate,
    CompanyAssociationList,
    CompanyDetail,
    CompanyList,
    CompanyCreate,
    CompanyUpdate,
    CompanyDelete,
    CompanyDisassociate)

app_name = 'pycompanies'
urlpatterns = [
    re_path(r'^$', CompanyList.as_view(), name='company_list_all'),
    re_path(r'^(?P<pk>\d+)/$', CompanyDetail.as_view(), name='detail'),
    re_path(r'^add/$', CompanyCreate.as_view(), name='add'),
    re_path(r'^(?P<pk>\d+)/edit/$', CompanyUpdate.as_view(), name='edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', CompanyDelete.as_view(), name='delete'),
    re_path(r'^(?P<pk>\d+)/disassociate/$', CompanyDisassociate.as_view(), name='disassociate'),
    re_path(r'^(?P<company>\d+)/associate/$', CompanyAssociate.as_view(), name='associate'),
    re_path(r'^asociarme/$', CompanyAssociationList.as_view(), name='association_list'),
    re_path(r'^admin/$', CompanyAdmin.as_view(), name='admin'),
]
