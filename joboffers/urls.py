from django.contrib.auth.decorators import login_required
from django.urls import re_path
from .views import (
  JobOfferAdminView, JobOfferCreateView, JobOfferDetailView, JobOfferHistoryView,
  JobOfferUpdateView, JobOfferRejectView, JobOfferAcceptView, JobOfferReactivateView
)


urlpatterns = [
    re_path(r'^admin/$', login_required(JobOfferAdminView.as_view()), name='admin'),
    re_path(r'^nueva/$', login_required(JobOfferCreateView.as_view()), name='add'),
    re_path(
      r'^(?P<slug>[\w-]+)/rechazar/$', login_required(JobOfferRejectView.as_view()), name='reject'
    ),
    re_path(
      r'^(?P<slug>[\w-]+)/aceptar/$', login_required(JobOfferAcceptView.as_view()), name='approve'
    ),
    re_path(
      r'^(?P<slug>[\w-]+)/desactivar/$', login_required(JobOfferAcceptView.as_view()),
      name='deactivate'
    ),
    re_path(
      r'^(?P<slug>[\w-]+)/reactivar/$', login_required(JobOfferReactivateView.as_view()),
      name='reactivate'
    ),
    re_path(
      r'^(?P<slug>[\w-]+)/solicitar-moderacion/$', login_required(JobOfferReactivateView.as_view()),
      name='request_moderation'
    ),
    re_path(
      r'^(?P<slug>[\w-]+)/historial/$', login_required(JobOfferHistoryView.as_view()),
      name='history'
    ),
    re_path(r'^(?P<slug>[\w-]+)/$', JobOfferDetailView.as_view(), name='view'),
    re_path(
      r'^(?P<slug>[\w-]+)/editar$', login_required(JobOfferUpdateView.as_view()),
      name='edit'
    )
]
