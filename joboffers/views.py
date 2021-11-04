from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .forms import JobOfferForm
from .models import JobOffer


class JobOfferCreateView(CreateView):
    model = JobOffer
    form_class = JobOfferForm
    success_url = reverse_lazy("joboffers_admin")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class JobOfferAdminView(ListView):
    # TODO: Implement
    model = JobOffer
