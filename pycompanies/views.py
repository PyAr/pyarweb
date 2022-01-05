from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.base import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from braces.views import LoginRequiredMixin

from pycompanies.forms import CompanyForm
from pycompanies.models import Company, UserCompanyProfile
from community.views import OwnedObject


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/company_detail.html'


class CompanyListView(ListView):
    template_name = 'companies/company_list.html'
    context_object_name = 'companies'

    def get_queryset(self):
        return Company.objects.all().order_by('?')

    def get_context_data(self, **kwargs):
        context = super(CompanyListView, self).get_context_data(**kwargs)
        if self.request.user.is_anonymous is False:
            try:
                context['own_company'] = UserCompanyProfile.objects.get(
                    user=self.request.user).company
                context['own_companies_count'] = self.request.user.companies.all().count()
                return context
            except UserCompanyProfile.DoesNotExist:
                return context


class CompanyCreateView(LoginRequiredMixin, CreateView):
    form_class = CompanyForm
    model = Company
    success_url = '/empresas/'
    template_name = 'companies/company_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CompanyCreateView, self).form_valid(form)


class CompanyUpdateView(LoginRequiredMixin, OwnedObject, UpdateView):
    form_class = CompanyForm
    model = Company
    template_name = 'companies/company_form.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
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
        If user is associated to a company, add to context the company and users information.
        """
        context = super(CompanyAdminView, self).get_context_data(**kwargs)
        context['page_title'] = _('Administrar Empresa')

        if self.request.user.is_anonymous is False:
            context['user'] = self.request.user
            try:
                user_company = UserCompanyProfile.objects.get(user=self.request.user)
                if user_company:
                    context['user_company_id'] = user_company.id
                    context['own_company'] = user_company.company
                    context['company_users'] = UserCompanyProfile.objects.filter(
                        company=context['own_company'])
                return context
            except UserCompanyProfile.DoesNotExist:
                return context


class CompanyAssociationListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'companies/company_association_list.html'
    queryset = Company.objects.all()
    context_object_name = 'companies'

    def get_queryset(self):
        """
        Filters companies if 'empresa' is passed as query param with the search value
        """
        queryset = super().get_queryset()
        if self.request.GET.get('empresa'):
            queryset = queryset.filter(
                name__icontains=self.request.GET['empresa'])
            return queryset

    def get_context_data(self, **kwargs):
        """
        Adds 'busqueda' to context if 'empresa' is passed as query param,
        in order to set the search input previous value.
        """
        context = super(CompanyAssociationListView, self).get_context_data(**kwargs)
        if self.request.GET.get('empresa'):
            context['busqueda'] = self.request.GET.get('empresa')
        return context


class CompanyDisassociateView(LoginRequiredMixin, DeleteView):
    model = UserCompanyProfile
    success_url = '/empresas/admin'
    template_name = 'companies/company_confirm_disassociate.html'

    def get_context_data(self, **kwargs):
        """
        Adds different messages to context, informing if it's the last associated.
        """
        context = super().get_context_data(**kwargs)
        context['company'] = context['object'].company
        users_quantity = context['object'].company.users.count()
        if (users_quantity == 1):
            context['message'] = "Esta es la última persona vinculada a esta empresa "\
                "¿Estás seguro que deseas desvincularla?"
        else:
            context['message'] = "¿Estás seguro que desea desvincular a "\
                f"{context['object'].user} de {context['object'].company.name}?"
        return context


def user_already_in_company(user):
    """
    Returns the user company profile if exists. If it doesn't, returns False.
    """
    try:
        user_company = UserCompanyProfile.objects.get(user=user)
        return user_company
    except UserCompanyProfile.DoesNotExist:
        return False


class CompanyAssociateView(LoginRequiredMixin, View):
    success_url = '/empresas/'

    def post(self, request, company):
        """
        Associates an user to the company if exists and is able to.
        """
        User = get_user_model()
        try:
            user = User.objects.get(username=request.POST['username'])
            user_company = user_already_in_company(user)
            company_to_associate = Company.objects.get(id=company)
            if user_company and company_to_associate == user_company.company:
                message = f'Le usuarie que desea vincular ya pertenece a {user_company.company}'
                messages.warning(request, message)
                return redirect('/empresas/admin/')
            elif user_company and company_to_associate != user_company.company:
                message = f'Le usuarie que ingresó esta vinculade a {user_company.company}.'
                messages.warning(request, message)
                return redirect('/empresas/admin/')
            else:
                association = UserCompanyProfile.objects.create(
                    user=user, company=company_to_associate)
                association.save()
                message = 'Le usuarie fue asociade correctamente.'
                messages.success(request, message)
                return redirect('/empresas/admin/')
        except User.DoesNotExist:
            messages.warning(request, 'Le usuarie que ingresó no existe.')
            return redirect('/empresas/admin/')
