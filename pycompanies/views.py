from braces.views import LoginRequiredMixin

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.base import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from community.views import OwnedObject
from joboffers.utils import get_visualizations_graph
from joboffers.models import EventType, JobOffer, JobOfferAccessLog
from pycompanies.forms import CompanyForm
from pycompanies.models import Company, UserCompanyProfile


ADMIN_URL = reverse_lazy('companies:admin')
ASSOCIATION_LIST_URL = reverse_lazy('companies:association_list')


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/company_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if UserCompanyProfile.objects.for_user(user=user) or user.is_superuser:
            context['can_view_analytics'] = True
        else:
            context['can_view_analytics'] = False

        return context


class CompanyListView(ListView):
    template_name = 'companies/company_list.html'
    context_object_name = 'companies'

    def get_queryset(self):
        return Company.objects.all().order_by('?')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user

        user_company = UserCompanyProfile.objects.for_user(user=self.request.user)
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

        user_company = UserCompanyProfile.objects.for_user(user=self.request.user)

        if user_company:
            context['user'] = self.request.user
            context['user_company_id'] = user_company.id
            context['own_company'] = user_company.company
            context['company_users'] = UserCompanyProfile.objects.filter(
              company=context['own_company']
            )

        return context

    def dispatch(self, request, *args, **kwargs):
        user_company = UserCompanyProfile.objects.for_user(user=self.request.user)
        if user_company:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(ASSOCIATION_LIST_URL)


def get_user_display_name(user):
    if user.first_name or user.last_name:
        return f"{user.first_name} {user.last_name}"
    else:
        return user.username


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
        companies = context['companies'] or []

        company_user_profiles = [company.users.all() for company in companies]

        owner_names = []

        for user_profiles in company_user_profiles:
            owner_names.append(
              [get_user_display_name(user_profile.user) for user_profile in user_profiles]
            )

        context['companies_and_owners'] = list(zip(companies, owner_names))

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


class CompanyAnalyticsView(DetailView):
    model = Company
    template_name = 'companies/company_analytics.html'

    def get_context_data(self, company):
        grouped_views_qs = JobOfferAccessLog.objects \
                                        .values('created_at__date', 'event_type') \
                                        .annotate(day_views=Count('id')) \
                                        .filter(joboffer__company=company) \
                                        .order_by('created_at__date')

        graphs = []

        for event_type in EventType:
            qs = grouped_views_qs.filter(event_type=event_type)

            if qs.exists():
                dates = qs.values_list('created_at__date', flat=True)
                day_views = qs.values_list('day_views', flat=True)

                graph = get_visualizations_graph(dates, day_views)
            else:
                graph = None

            graphs.append([event_type.label, graph])

        totals_qs = JobOfferAccessLog.objects.filter(joboffer__company=company) \
                                             .values('joboffer', 'event_type') \
                                             .annotate(total_views=Count('id'))

        joboffer_data = []

        for joboffer in JobOffer.objects.filter(company=company).order_by('-created_at'):
            data = [joboffer]

            qs = totals_qs.filter(joboffer=joboffer)
            totals_by_event_type = dict(qs.values_list('event_type', 'total_views'))

            for event_type in EventType:
                data.append(totals_by_event_type.get(event_type, 0))

            joboffer_data.append(data)

        return {'company': company, 'graphs': graphs, 'joboffers_data': joboffer_data}

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        user = request.user

        owner_profile = UserCompanyProfile.objects.for_user(user=user, company=company)
        if owner_profile or user.is_superuser:
            context = self.get_context_data(company)

            return render(request, self.template_name, context=context)
        else:
            raise PermissionDenied()
