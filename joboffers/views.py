from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, RedirectView, View, FormView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView

from pycompanies.models import Company
from .forms import JobOfferForm, JobOfferCommentForm
from .joboffer_actions import (
    CODE_CREATE, CODE_EDIT, CODE_HISTORY, CODE_REJECT, CODE_REACTIVATE, CODE_DEACTIVATE,
    CODE_REQUEST_MODERATION, CODE_APPROVE, get_valid_actions, validate_action
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
        "css_classes": ["btn-default"],
        "icon_class": "glyphicon-pencil"
    }
}


class JobOfferCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = JobOffer
    form_class = JobOfferForm
    success_message = _(
        "Oferta creada correctamente. A continuación debe confirmarla para que sea revisada por el"
        "equipo de moderación y quede activa."
    )

    def get(self, request, *args, **kwargs):
        if not validate_action(CODE_CREATE, request.user):
            return PermissionDenied()

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("joboffers:view", kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class JobOfferDetailView(LoginRequiredMixin, DetailView):
    model = JobOffer

    def get_action_buttons(self):
        valid_actions = get_valid_actions(self.object, self.request.user)

        return [ACTION_BUTTONS[action_name] for action_name in valid_actions]

    def get_context_data(self, object):
        ctx = super().get_context_data()
        ctx['action_buttons'] = self.get_action_buttons()
        return ctx


class JobOfferUpdateView(LoginRequiredMixin, UpdateView):
    model = JobOffer
    form_class = JobOfferForm
    success_url = "joboffers:view"

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url, args=args, kwargs=kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        form.instance.state = OfferState.MODERATION
        # TODO: Avoid changing the state if no fields changed
        return super().form_valid(form)


class JobOfferAdminView(LoginRequiredMixin, ListView):
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
        return ctx


class TransitionView(SingleObjectMixin, View):
    model = JobOffer
    redirect_to_pattern: str
    success_message: str

    def update_object(self):
        raise NotImplementedError()

    def get(self, request, *args, **kwargs):
        offer = self.get_object()

        if not validate_action(CODE_REQUEST_MODERATION, request.user, offer):
            raise PermissionDenied()

        self.update_object(offer)

        messages.success(request, self.success_message)

        target_url = reverse(self.redirect_to_pattern, args=args, kwargs=kwargs)
        return HttpResponseRedirect(target_url)


class JobOfferRejectView(
        LoginRequiredMixin, SuccessMessageMixin, SingleObjectMixin, FormView
):
    action_code = CODE_REQUEST_MODERATION
    model = JobOffer  # SingleObjectMixin needs this to retrieve the joboffer
    form_class = JobOfferCommentForm
    template_name = 'joboffers/joboffer_reject.html'
    success_message = _(
        "Oferta creada correctamente. A continuación debe confirmarla para que sea revisada por el"
        "equipo de moderación y quede activa."
    )

    def get_object(self, queryset=None):
        offer = super().get_object(queryset)

        # TODO: Move this to a mixin
        if not validate_action(self.action_code, self.request.user, offer):
            raise PermissionDenied()

        return offer

    def get_initial(self):
        initial = super().get_initial()
        initial['joboffer'] = self.object
        return initial

    def get_form(self, form_class=None):
        return super().get_form(form_class)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not validate_action(CODE_CREATE, request.user):
            return PermissionDenied()

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


class JobOfferAcceptView(LoginRequiredMixin, TransitionView):
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
