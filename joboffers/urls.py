from django.views.generic.detail import DetailView
from django.urls import re_path
from .models import JobOffer


urlpatterns = [
    re_path(r'^(?P<slug>[\w-]+)/$', DetailView.as_view(model=JobOffer), name='jobsoffer_view'),
]
