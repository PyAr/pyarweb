from django.conf.urls import patterns, url

from .views import (
    CompanyDetail,
    CompanyList,
    CompanyCreate,
    CompanyUpdate,
    CompanyDelete)

urlpatterns = patterns(
    '',
    url(r'^$', CompanyList.as_view(), name='company_list_all'),
    url(r'^(?P<pk>\d+)/$', CompanyDetail.as_view(), name='detail'),
    url(r'^add/$', CompanyCreate.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/edit/$', CompanyUpdate.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', CompanyDelete.as_view(), name='delete'),
)
