from django.urls import re_path

from .views import (
    CompanyDetail,
    CompanyList,
    CompanyCreate,
    CompanyUpdate,
    CompanyDelete)

app_name = 'pycompanies'
urlpatterns = [
    re_path(r'^$', CompanyList.as_view(), name='company_list_all'),
    re_path(r'^(?P<pk>\d+)/$', CompanyDetail.as_view(), name='detail'),
    re_path(r'^add/$', CompanyCreate.as_view(), name='add'),
    re_path(r'^(?P<pk>\d+)/edit/$', CompanyUpdate.as_view(), name='edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', CompanyDelete.as_view(), name='delete'),
]
