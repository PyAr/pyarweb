from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from pycompanies.models import Company
from .forms import JobOfferForm
from .joboffer_actions import (
    CODE_EDIT, CODE_REJECT, CODE_REACTIVATE, CODE_DEACTIVATE,
    CODE_REQUEST_MODERATION, CODE_APPROVE
)
from .models import JobOffer


class JobOfferCreateView(CreateView):
    model = JobOffer
    form_class = JobOfferForm

    def get_success_url(self):
        return reverse("joboffers:view", kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


ACTION_BUTTONS = {
    CODE_EDIT: {
        "target_url": 'joboffers:edit',
        "text": _('Editar'),
        "css_classes": ["btn-success"],
        "icon_class": "glyphicon-pencil"
    },
    CODE_REJECT: {
        "target_url": 'joboffers:reject',
        "text": _('Rechazar'),
        "css_classes": ["btn-danger"],
        "icon_class": "glyphicon-thumbs-down"
    },
    # CODE_COMMENT: {
    #     "target_url": 'joboffers:edit',
    #     "text": _('Comentar'),
    #     "css_classes": ["btn-default"],
    #     "icon_class": "glyphicon-comment"
    # },
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
        "text": _('Solicitar Moderación'),
        "css_classes": ["btn-secondary"],
        "icon_class": "glyphicon-eye-open"
    },
    CODE_APPROVE: {
        "target_url": 'joboffers:approve',
        "text": _('Aprobar'),
        "css_classes": ["btn-default"],
        "icon_class": "glyphicon-pencil"
    }
}


class JobOfferDetailView(DetailView):
    model = JobOffer

    def get_action_buttons(self):
        # TODO: call get_valid_actions() instead
        valid_actions = [CODE_EDIT, CODE_REJECT]

        return [ACTION_BUTTONS[action_name] for action_name in valid_actions]

    def get_context_data(self, object):
        ctx = super().get_context_data()
        ctx['action_buttons'] = self.get_action_buttons()
        return ctx


class JobOfferUpdateView(UpdateView):
    model = JobOffer
    form_class = JobOfferForm
    success_url = "joboffers:view"

    def get_success_url(self, *args, **kwargs):
        return reverse('joboffers:view', kwargs=self.kwargs)

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
        return ctx


class JobOfferRejectView(RedirectView):
    pattern_name = 'joboffers:view'


class JobOfferAcceptView(RedirectView):
    pattern_name = 'joboffers:view'


class JobOfferReactivateView(RedirectView):
    pattern_name = 'joboffers:view'


class JobOfferDeactivateView(RedirectView):
    pattern_name = 'joboffers:view'


class JobOfferRequestModerationView(RedirectView):
    pattern_name = 'joboffers:view'
