from django.urls import path

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
    path('', CompanyListView.as_view(), name='company_list_all'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='detail'),
    path('agregar/', CompanyCreateView.as_view(), name='add'),
    path('<int:pk>/editar/', CompanyUpdateView.as_view(), name='edit'),
    path('<int:pk>/eliminar/', CompanyDeleteView.as_view(), name='delete'),
    path('<int:company>/asociar/', CompanyAssociateView.as_view(), name='associate'),
    path('asociarme/', CompanyAssociationListView.as_view(), name='association_list'),
    path('admin/', CompanyAdminView.as_view(), name='admin'),
    path('<int:pk>/desasociar/', CompanyDisassociateView.as_view(), name='disassociate'),
    path('<int:pk>/analitica/', CompanyAnalyticsView.as_view(), name='analytics')
]
