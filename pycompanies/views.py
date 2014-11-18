from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from braces.views import LoginRequiredMixin

from pycompanies.forms import CompanyForm
from pycompanies.models import Company
from community.views import OwnedObject


class CompanyDetail(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'companies/company_detail.html'


class CompanyList(LoginRequiredMixin, ListView):
    template_name = 'companies/company_list.html'
    context_object_name = 'companies'

    def get_queryset(self):
        return Company.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CompanyList, self).get_context_data(**kwargs)
        context['own_companies_count'] = self.request.user.companies.all() \
            .count()
        return context


class CompanyCreate(LoginRequiredMixin, CreateView):
    form_class = CompanyForm
    model = Company
    success_url = '/empresas/'
    template_name = 'companies/company_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CompanyCreate, self).form_valid(form)


class CompanyUpdate(LoginRequiredMixin, OwnedObject, UpdateView):
    form_class = CompanyForm
    model = Company
    template_name = 'companies/company_form.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdate, self).get_context_data(**kwargs)
        context['page_title'] = _('Editar compania')
        return context


class CompanyDelete(LoginRequiredMixin, OwnedObject, DeleteView):
    model = Company
    success_url = '/empresas/'
    template_name = 'companies/company_confirm_delete.html'
