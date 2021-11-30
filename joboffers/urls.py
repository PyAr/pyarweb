from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.urls import re_path
from .models import JobOffer
from .views import JobOfferAdminView, JobOfferCreateView, JobOfferUpdateView


urlpatterns = [
    re_path(r'^admin/$', login_required(JobOfferAdminView.as_view()), name='admin'),
    re_path(r'^nueva/$', login_required(JobOfferCreateView.as_view()), name='add'),
    re_path(r'^(?P<slug>[\w-]+)/$', DetailView.as_view(model=JobOffer), name='view'),
    re_path(
      r'^(?P<slug>[\w-]+)/editar$', login_required(JobOfferUpdateView.as_view()),
      name='edit'
    )
]
