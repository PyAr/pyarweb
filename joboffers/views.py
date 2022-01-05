from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from pycompanies.models import Company, UserCompanyProfile
from .forms import JobOfferForm
from .models import JobOffer


class JobOfferCreateView(CreateView):
    model = JobOffer
    form_class = JobOfferForm
    success_url = reverse_lazy("joboffers:admin")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        try:
            user_company = UserCompanyProfile.objects.get(user=self.request.user)
            self.initial.update({'company': user_company.company})
            return self.initial
        except UserCompanyProfile.DoesNotExist:
            return self.initial


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
    paginate_by = 10

    def get_queryset(self):
        # TODO: Implement queryset filtering for the company
        # TODO: Implement reverse ordering by date
        return super().get_queryset()

    def get_context_data(self, *args, **kwargs):
        # TODO: Implement fetching the company
        # TODO: Implement redirect when no company associated
        ctx = super().get_context_data()
        ctx['company'] = Company.objects.first()
        return ctx
