from braces.views import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.base import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from community.views import OwnedObject
from pycompanies.forms import CompanyForm
from pycompanies.models import Company, UserCompanyProfile


ADMIN_URL = reverse_lazy('companies:admin')
ASSOCIATION_LIST_URL = reverse_lazy('companies:association_list')


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/company_detail.html'


class CompanyListView(ListView):
    template_name = 'companies/company_list.html'
    context_object_name = 'companies'

    def get_queryset(self):
        return Company.objects.all().order_by('?')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_company = UserCompanyProfile.objects.filter(user=self.request.user).first()
        if self.request.user.is_anonymous is False and user_company:
            context['own_company'] = user_company.company
        return context


class CompanyCreateView(LoginRequiredMixin, CreateView):
    form_class = CompanyForm
    model = Company
    success_url = '/empresas/'
    template_name = 'companies/company_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CompanyUpdateView(LoginRequiredMixin, OwnedObject, UpdateView):
    form_class = CompanyForm
    model = Company
    template_name = 'companies/company_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Editar Empresa')
        return context


class CompanyDeleteView(LoginRequiredMixin, OwnedObject, DeleteView):
    model = Company
    success_url = '/empresas/'
    template_name = 'companies/company_confirm_delete.html'


class CompanyAdminView(LoginRequiredMixin, TemplateView):
    model = Company
    template_name = 'companies/company_admin.html'

    def get_context_data(self, **kwargs):
        """
        If user is associated to a company, add company and user's information to context
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Administrar Empresa')

        if self.request.user.is_anonymous is False:
            context['user'] = self.request.user
            user_company = UserCompanyProfile.objects.filter(user=self.request.user).first()
            if user_company:
                context['user_company_id'] = user_company.id
                context['own_company'] = user_company.company
                context['company_users'] = UserCompanyProfile.objects.filter(
                    company=context['own_company'])
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous is False:
            user_company = UserCompanyProfile.objects.filter(user=self.request.user).first()
            if not user_company:
                return redirect(ASSOCIATION_LIST_URL)

        return super().dispatch(request, *args, **kwargs)


class CompanyAssociationListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'companies/company_association_list.html'
    queryset = Company.objects.all()
    context_object_name = 'companies'

    def get_queryset(self):
        """
        Filter companies if 'empresa' is passed as query param with the search value
        """
        queryset = super().get_queryset()
        if self.request.GET.get('empresa'):
            queryset = queryset.filter(
                name__icontains=self.request.GET['empresa'])
            return queryset

    def get_context_data(self, **kwargs):
        """
        Add 'busqueda' to context if 'empresa' is passed as query param,
        in order to set the search input previous value.
        """
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('empresa'):
            context['busqueda'] = self.request.GET.get('empresa')
        return context


class CompanyDisassociateView(LoginRequiredMixin, DeleteView):
    model = UserCompanyProfile
    success_url = '/empresas/admin'
    template_name = 'companies/company_confirm_disassociate.html'

    def get_context_data(self, **kwargs):
        """
        Add different messages to context, informing if it's the last associated.
        """
        context = super().get_context_data(**kwargs)
        context['company'] = context['object'].company
        users_quantity = context['object'].company.users.count()
        if users_quantity == 1:
            context['message'] = ('Esta es la última persona vinculada a esta empresa '
                                  '¿Estás seguro que deseas desvincularla?')
        else:
            context['message'] = ('¿Estás seguro que deseas desvincular a '
                                  f'{context["object"].user} de {context["object"].company.name}?')
        return context


class CompanyAssociateView(LoginRequiredMixin, View):
    success_url = '/empresas/'

    def post(self, request, company):
        """
        Associate an user to the company if exists and is able to.
        """
        User = get_user_model()
        user = User.objects.filter(username=request.POST['username']).first()
        if user:
            user_company = UserCompanyProfile.objects.for_user(user)
            company_to_associate = Company.objects.get(id=company)
            if user_company and company_to_associate == user_company.company:
                message = f'Le usuarie que desea vincular ya pertenece a {user_company.company}'
                messages.warning(request, message)
            elif user_company and company_to_associate != user_company.company:
                message = f'Le usuarie que ingresó esta vinculade a {user_company.company}.'
                messages.warning(request, message)
            else:
                association = UserCompanyProfile.objects.create(user=user,
                                                                company=company_to_associate)
                association.save()
                message = 'Le usuarie fue asociade correctamente.'
                messages.success(request, message)
        else:
            messages.warning(request, 'Le usuarie que ingresaste no existe.')
        return redirect(ADMIN_URL)
