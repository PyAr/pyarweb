from django.urls import re_path
from .views import (
  JobOfferAdminView, JobOfferCreateView, JobOfferDetailView, JobOfferHistoryView,
  JobOfferUpdateView, JobOfferRejectView, JobOfferApproveView, JobOfferReactivateView,
  JobOfferRequestModerationView
)


urlpatterns = [
    re_path(r'^admin/$', JobOfferAdminView.as_view(), name='admin'),
    re_path(r'^nueva/$', JobOfferCreateView.as_view(), name='add'),
    re_path(
      r'^(?P<slug>[\w-]+)/rechazar/$', JobOfferRejectView.as_view(), name='reject'
    ),
    re_path(
      r'^(?P<slug>[\w-]+)/aceptar/$', JobOfferApproveView.as_view(), name='approve'
    ),
    re_path(
      r'^(?P<slug>[\w-]+)/desactivar/$', JobOfferApproveView.as_view(),
      name='deactivate'
    ),
    re_path(
      r'^(?P<slug>[\w-]+)/reactivar/$', JobOfferReactivateView.as_view(),
      name='reactivate'
    ),
    re_path(
      r'^(?P<slug>[\w-]+)/solicitar-moderacion/$', JobOfferRequestModerationView.as_view(),
      name='request_moderation'
    ),
    re_path(
      r'^(?P<slug>[\w-]+)/historial/$', JobOfferHistoryView.as_view(),
      name='history'
    ),
    re_path(r'^(?P<slug>[\w-]+)/$', JobOfferDetailView.as_view(), name='view'),
    re_path(
      r'^(?P<slug>[\w-]+)/editar$', JobOfferUpdateView.as_view(),
      name='edit'
    )
]
