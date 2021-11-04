from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.urls import re_path
from .models import JobOffer
from .views import JobOfferAdminView, JobOfferCreateView


urlpatterns = [
    re_path(r'^admin/$', login_required(JobOfferAdminView.as_view()), name='joboffers_admin'),
    re_path(r'^nueva/$', login_required(JobOfferCreateView.as_view()), name='joboffers_add'),
    re_path(r'^(?P<slug>[\w-]+)/$', DetailView.as_view(model=JobOffer), name='joboffers_view'),
]
