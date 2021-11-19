from dal import autocomplete
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from taggit.models import Tag

from pycompanies.models import Company
from .forms import JobOfferForm, SearchForm
from .models import JobOffer


class JobOfferCreateView(CreateView):
    model = JobOffer
    form_class = JobOfferForm
    success_url = reverse_lazy("joboffers:admin")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class JobOfferUpdateView(UpdateView):
    model = JobOffer
    form_class = JobOfferForm
    success_url = reverse_lazy("joboffers:admin")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class JobOfferAdminView(ListView):
    template_name = 'joboffers/joboffer_admin.html'
    model = JobOffer

    def get_queryset(self):
        # TODO: Implement queryset filtering for the company
        # TODO: Implement reverse ordering by date
        return super().get_queryset()

    def get_context_data(self, *args, **kwargs):
        # TODO: Implement fetching the company
        # TODO: Implement redirect when no company associated
        ctx = super().get_context_data()
        ctx['company'] = Company.objects.first()
        ctx['search_form'] = SearchForm()

        return ctx


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
