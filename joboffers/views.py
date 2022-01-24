from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, RedirectView, View, FormView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView

from pycompanies.models import Company, UserCompanyProfile
from .forms import JobOfferForm, JobOfferCommentForm
from .joboffer_actions import (
    CODE_CREATE, CODE_EDIT, CODE_HISTORY, CODE_REJECT, CODE_REACTIVATE, CODE_DEACTIVATE,
    CODE_REQUEST_MODERATION, CODE_APPROVE, get_valid_actions
)
from .models import JobOffer, JobOfferComment, OfferState


ACTION_BUTTONS = {
    CODE_HISTORY: {
        "target_url": 'joboffers:history',
        "text": _('Historial'),
        "css_classes": ["btn-info"],
        "icon_class": "glyphicon-time"
    },
    CODE_EDIT: {
        "target_url": 'joboffers:edit',
        "text": _('Editar'),
        "css_classes": ["btn-default"],
        "icon_class": "glyphicon-pencil"
    },
    CODE_REJECT: {
        "target_url": 'joboffers:reject',
        "text": _('Rechazar'),
        "css_classes": ["btn-danger"],
        "icon_class": "glyphicon-thumbs-down"
    },
    CODE_REACTIVATE: {
        "target_url": 'joboffers:reactivate',
        "text": _('Volver a Activar'),
        "css_classes": ["btn-default"],
        "icon_class": "glyphicon-arrow-up"
    },
    CODE_DEACTIVATE: {
        "target_url": 'joboffers:deactivate',
        "text": _('Desactivar'),
        "css_classes": ["btn-warning"],
        "icon_class": "glyphicon-minus-sign"
    },
    CODE_REQUEST_MODERATION: {
        "target_url": 'joboffers:request_moderation',
        "text": _('Confirmar'),
        "css_classes": ["btn-success"],
        "icon_class": "glyphicon-eye-open"
    },
    CODE_APPROVE: {
        "target_url": 'joboffers:approve',
        "text": _('Aprobar'),
        "css_classes": ["btn-success"],
        "icon_class": "glyphicon-pencil"
    }
}


class JobOfferObjectMixin(SingleObjectMixin):
    """
    Adds permission checking to the matching joboffer
    """

    action_code: str

    def get_object(self, queryset=None):
        offer = super().get_object(queryset)

        if not self.action_code:
            raise ValueError("Missing 'action_code' for the current class")

        valid_actions = get_valid_actions(self.request.user, offer.company, offer.state)

        if self.action_code not in valid_actions:
            raise PermissionDenied()

        return offer


def get_user_company(user):
    if user.is_anonymous:
        None
    else:
        company_profile_qs = UserCompanyProfile.objects.filter(user=user)
        if company_profile_qs.exists():
            return company_profile_qs.first().company


class JobOfferCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    action_code = CODE_CREATE
    model = JobOffer
    form_class = JobOfferForm
    success_message = _(
        "Oferta creada correctamente. A continuación debe confirmarla para que sea revisada por el"
        "equipo de moderación y quede activa."
    )

    def get(self, request, *args, **kwargs):
        company = get_user_company(request.user)

        valid_actions = get_valid_actions(self.request.user, company, OfferState.NEW)

        if self.action_code not in valid_actions:
            raise PermissionDenied()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        company = get_user_company(request.user)

        valid_actions = get_valid_actions(self.request.user, company, OfferState.NEW)

        if self.action_code not in valid_actions:
            raise PermissionDenied()

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("joboffers:view", kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        user_company = UserCompanyProfile.objects.filter(user=self.request.user).first()
        if user_company:
            self.initial.update({'company': user_company.company})

        return self.initial


class JobOfferDetailView(DetailView):
    model = JobOffer

    def get_action_buttons(self):
        joboffer = self.object
        valid_actions = get_valid_actions(self.request.user, joboffer.company, joboffer.state)

        return [ACTION_BUTTONS[action_name] for action_name in valid_actions]

    def get_context_data(self, object):
        ctx = super().get_context_data()
        ctx['action_buttons'] = self.get_action_buttons()
        return ctx


class JobOfferUpdateView(LoginRequiredMixin, JobOfferObjectMixin, UpdateView):
    action_code = CODE_EDIT
    model = JobOffer
    form_class = JobOfferForm
    success_url = "joboffers:view"

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url, kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.state = OfferState.DEACTIVATED
        return super().form_valid(form)


class JobOfferAdminView(LoginRequiredMixin, ListView):
    template_name = 'joboffers/joboffer_admin.html'
    model = JobOffer
    paginate_by = 10

    def get_queryset(self):
        # TODO: Implement queryset filtering for the company
        query = self.request.GET.get('q')

        if query:
            filtering_q = Q(title__icontains=query) | Q(tags__name__iexact=query)
        else:
            filtering_q = Q()

        qs = super().get_queryset()

        return (
            qs
            .order_by('-created_at')
            .filter(
                filtering_q
            )
        )

    def get_context_data(self, *args, **kwargs):
        # TODO: Implement fetching the company
        # TODO: Implement redirect when no company associated
        ctx = super().get_context_data()
        ctx['company'] = Company.objects.first()
        return ctx


class TransitionView(JobOfferObjectMixin, View):
    model = JobOffer
    redirect_to_pattern: str
    success_message: str

    def update_object(self):
        raise NotImplementedError()

    def get(self, request, *args, **kwargs):
        offer = self.get_object()

        self.update_object(offer)

        messages.success(request, self.success_message)

        target_url = reverse(self.redirect_to_pattern, args=args, kwargs=kwargs)
        return HttpResponseRedirect(target_url)


class JobOfferRejectView(
        LoginRequiredMixin, SuccessMessageMixin, JobOfferObjectMixin, FormView
):
    action_code = CODE_REJECT
    model = JobOffer  # SingleObjectMixin needs this to retrieve the joboffer
    form_class = JobOfferCommentForm
    template_name = 'joboffers/joboffer_reject.html'
    success_message = _(
        "Oferta rechazada. Se marca como desactivada para que el publicador la revise. "
    )

    def get_initial(self):
        initial = super().get_initial()
        initial['joboffer'] = self.object
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        self.object.state = OfferState.DEACTIVATED
        self.object.save()
        form.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("joboffers:view", kwargs={'slug': self.object.slug})


class JobOfferApproveView(LoginRequiredMixin, TransitionView):
    action_code = CODE_APPROVE
    redirect_to_pattern = 'joboffers:view'
    success_message = _('Oferta aceptada y activada. En caso de error puede rechazarla.')

    def update_object(self, offer):
        offer.state = OfferState.ACTIVE
        offer.save()


class JobOfferReactivateView(LoginRequiredMixin, RedirectView):
    pattern_name = 'joboffers:view'


class JobOfferDeactivateView(LoginRequiredMixin, RedirectView):
    pattern_name = 'joboffers:view'


class JobOfferRequestModerationView(LoginRequiredMixin, TransitionView):
    action_code = CODE_REQUEST_MODERATION
    redirect_to_pattern = 'joboffers:view'
    success_message = _(
        "Oferta enviada a moderación. El equipo de moderadores lo revisará y pasará a estar"
        "activa si es correcta. Revise está misma página para ver el estado."
    )

    def update_object(self, offer):
        offer.state = OfferState.MODERATION
        offer.save()


class JobOfferHistoryView(LoginRequiredMixin, ListView):
    model = JobOfferComment
    template_name = "joboffers/history.html"
