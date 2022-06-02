import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.syndication.views import Feed
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, View, FormView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView

from community.views import FilterableList
from pycompanies.models import UserCompanyProfile
from .constants import (
  ACTION_BUTTONS,
  APPROVED_MAIL_SUBJECT,
  APPROVED_MAIL_BODY,
  CODE_ANALYTICS,
  CODE_APPROVE,
  CODE_CREATE,
  CODE_DEACTIVATE,
  CODE_EDIT,
  CODE_HISTORY,
  CODE_REACTIVATE,
  CODE_REJECT,
  CODE_REQUEST_MODERATION,
  PUBLISHER_FAILED_ERROR,
  REACTIVATED_MAIL_BODY,
  REACTIVATED_MAIL_SUBJECT,
  REJECTED_MAIL_SUBJECT,
  REJECTED_MAIL_BODY,
  STATE_LABEL_CLASSES,
  TELEGRAM_APPROVED_MESSAGE,
  TELEGRAM_MODERATION_MESSAGE,
  TELEGRAM_REJECT_MESSAGE
)
from .forms import JobOfferForm, JobOfferCommentForm
from .joboffer_actions import get_valid_actions
from .models import EventType, JobOffer, JobOfferAccessLog, JobOfferHistory, OfferState
from .telegram_api import send_notification_to_moderators
from .publishers import publish_to_all_social_networks
from .utils import get_visualization_data, get_visualizations_graph, send_mail_to_publishers


class JobOfferObjectMixin(SingleObjectMixin):
    """
    Adds permission checking to the matching joboffer
    """

    action_code: str

    def get_object(self, queryset=None):
        offer = super().get_object(queryset)

        if not self.action_code:
            raise ValueError("Missing 'action_code' for the current class")

        valid_actions = get_valid_actions(self.request.user, offer)

        if self.action_code not in valid_actions:
            raise PermissionDenied()

        return offer


class JobOfferCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    action_code = CODE_CREATE
    model = JobOffer
    form_class = JobOfferForm
    success_message = _(
        'Oferta creada correctamente. A continuación debe confirmarla para que sea revisada por el'
        'equipo de moderación y quede activa.'
    )

    def get(self, request, *args, **kwargs):
        user_company = UserCompanyProfile.objects.for_user(request.user)

        if not user_company:
            message = ("No estas relacionade a ninguna empresa. Asociate a una para poder "
                       "crear una oferta de trabajo.")
            messages.warning(request, message)
            target_url = reverse('companies:association_list')
            return HttpResponseRedirect(target_url)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        valid_actions = get_valid_actions(self.request.user, None)

        if self.action_code not in valid_actions:
            raise PermissionDenied()

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('joboffers:view', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        user_company = UserCompanyProfile.objects.for_user(self.request.user)
        if user_company:
            self.initial.update({'company': user_company.company})

        return self.initial


class JobOfferDetailView(DetailView):
    model = JobOffer

    def get_action_buttons(self):
        joboffer = self.object
        valid_actions = get_valid_actions(self.request.user, joboffer)

        return [ACTION_BUTTONS[action_name] for action_name in valid_actions]

    def get_context_data(self, object):
        ctx = super().get_context_data()
        ctx['action_buttons'] = self.get_action_buttons()
        ctx['state_label_class'] = STATE_LABEL_CLASSES[object.state]
        ctx['OfferState'] = OfferState
        return ctx

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        joboffer = self.object
        joboffer.track_visualization(request.session, event_type=EventType.DETAIL_VIEW)

        return response


class JobOfferUpdateView(LoginRequiredMixin, JobOfferObjectMixin, UpdateView):
    action_code = CODE_EDIT
    model = JobOffer
    form_class = JobOfferForm
    success_url = 'joboffers:view'

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url, kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.state = OfferState.DEACTIVATED
        return super().form_valid(form)

    def get_initial(self):
        user_company = UserCompanyProfile.objects.for_user(self.request.user)
        if user_company:
            self.initial.update({'company': user_company.company})

        return self.initial


class JobOfferAdminView(LoginRequiredMixin, ListView):
    template_name = 'joboffers/joboffer_admin.html'
    model = JobOffer
    paginate_by = 10

    def get_queryset(self):
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
                Q(company=self.company) & filtering_q
            )
        )

    def get(self, request, *args, **kwargs):
        user_company = UserCompanyProfile.objects.for_user(request.user)

        if not user_company:
            message = ("No estas relacionade a ninguna empresa. Asociate a una para poder "
                       "crear una oferta de trabajo.")
            messages.warning(request, message)
            target_url = reverse('companies:association_list')
            return HttpResponseRedirect(target_url)

        self.company = user_company.company
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data()
        ctx['company'] = self.company
        ctx['q'] = self.request.GET.get('q')

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
        'Oferta rechazada. Se marca como desactivada para que el publicador la revise. '
    )

    def get_initial(self):
        initial = super().get_initial()
        initial['joboffer'] = self.object
        return initial

    def form_valid(self, form):
        offer_comment = form.instance
        offer = self.object
        user = self.request.user

        offer_comment.created_by = user
        offer_comment.modified_by = user
        offer.state = OfferState.REJECTED
        offer.save()
        form.save()

        subject = REJECTED_MAIL_SUBJECT
        body = REJECTED_MAIL_BODY.format(
          reason=offer_comment.get_comment_type_display(),
          text=offer_comment.text,
          title=offer.title
        )

        send_mail_to_publishers(offer, subject, body)

        moderators_message = TELEGRAM_REJECT_MESSAGE.format(
          offer_url=offer.get_absolute_url(),
          username=user.username
        )

        send_notification_to_moderators(moderators_message)
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
        return reverse('joboffers:view', kwargs={'slug': self.object.slug})


class JobOfferApproveView(LoginRequiredMixin, TransitionView):
    action_code = CODE_APPROVE
    redirect_to_pattern = 'joboffers:view'
    success_message = _('Oferta aceptada y activada. En caso de error puede rechazarla.')

    def update_object(self, offer):
        offer.state = OfferState.ACTIVE
        offer.modified_by = self.request.user
        offer.save()

        user = self.request.user

        send_mail_to_publishers(
          offer,
          APPROVED_MAIL_SUBJECT,
          APPROVED_MAIL_BODY.format(title=offer.title)
        )

        moderators_message = TELEGRAM_APPROVED_MESSAGE.format(
          offer_url=offer.get_absolute_url(),
          username=user.username
        )

        send_notification_to_moderators(moderators_message)

        publishers_failed = publish_to_all_social_networks(offer)

        for publisher_failed in publishers_failed:
            messages.add_message(
              self.request,
              messages.ERROR,
              PUBLISHER_FAILED_ERROR.format(publisher=publisher_failed)
            )


class JobOfferReactivateView(LoginRequiredMixin, TransitionView):
    action_code = CODE_REACTIVATE
    redirect_to_pattern = 'joboffers:view'
    success_message = _('Oferta reactivada.')

    def update_object(self, offer):
        offer.state = OfferState.ACTIVE
        offer.save()

        send_mail_to_publishers(
          offer,
          REACTIVATED_MAIL_SUBJECT,
          REACTIVATED_MAIL_BODY.format(title=offer.title)
        )


class JobOfferDeactivateView(LoginRequiredMixin, TransitionView):
    action_code = CODE_DEACTIVATE
    redirect_to_pattern = 'joboffers:view'
    success_message = _('Oferta desactivada.')

    def update_object(self, offer):
        offer.state = OfferState.DEACTIVATED
        offer.save()


class JobOfferRequestModerationView(LoginRequiredMixin, TransitionView):
    action_code = CODE_REQUEST_MODERATION
    redirect_to_pattern = 'joboffers:view'
    success_message = _(
        'Oferta enviada a moderación. El equipo de moderadores lo revisará y pasará a estar '
        'activa si es correcta. Revise está misma página para ver el estado.'
    )

    def update_object(self, offer):
        offer.state = OfferState.MODERATION
        offer.save()

        moderators_message = TELEGRAM_MODERATION_MESSAGE.format(
          offer_url=offer.get_absolute_url()
        )

        send_notification_to_moderators(moderators_message)


class JobOfferHistoryView(LoginRequiredMixin, JobOfferObjectMixin, ListView):
    action_code = CODE_HISTORY
    paginate_by = 10
    template_name = "joboffers/joboffer_history.html"
    HIDDEN_JOBOFFER_FIELDS = ['slug', 'fields_hash']

    def get_queryset(self):
        """
        Get the queryset for all the history objects related to an offer
        """
        return JobOfferHistory.objects.for_offer(joboffer=self.object)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['JobOfferHistory'] = JobOfferHistory
        ctx['OfferState'] = OfferState
        ctx['HIDDEN_JOBOFFER_FIELDS'] = self.HIDDEN_JOBOFFER_FIELDS

        return ctx

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(JobOffer.objects.all())
        response = super().get(request, *args, **kwargs)
        return response


class JobOfferListView(ListView, FilterableList):
    model = JobOffer
    template_name = 'joboffers/joboffer_list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')

        if search:
            search_filter = Q(title__icontains=search) | Q(description__icontains=search)
        else:
            search_filter = Q()

        if self.request.GET.get('active') == 'false':
            joboffer_queryset = queryset.filter(
                search_filter,
                state__in=[OfferState.ACTIVE, OfferState.EXPIRED])
            ordered_offers = joboffer_queryset.order_by('-modified_at')
        else:
            joboffer_queryset = queryset.filter(search_filter, state=OfferState.ACTIVE)
            ordered_offers = joboffer_queryset.order_by('-company__rank', '-modified_at')

        return ordered_offers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('active') == 'false':
            context['active'] = True
        else:
            context['active'] = False

        if self.request.GET.get('search'):
            context['search'] = self.request.GET.get('search')

        self.context = context

        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        joboffers = self.context['page_obj'].object_list

        for joboffer in joboffers:
            joboffer.track_visualization(request.session, event_type=EventType.LISTING_VIEW)

        return response


class TrackContactInfoView(SingleObjectMixin, View):
    model = JobOffer

    def post(self, request, **kwargs):
        joboffer = self.get_object()

        joboffer.track_visualization(request.session, event_type=EventType.CONTACT_INFO_VIEW)

        return HttpResponse(status=204)


class JobOfferAnalytics(JobOfferObjectMixin, View):
    action_code = CODE_ANALYTICS
    model = JobOffer
    template_name = 'joboffers/joboffer_analytics.html'

    def get_context_data(self, joboffer):
        log_queryset = JobOfferAccessLog.objects.filter(joboffer=joboffer)

        totals = []
        graphs = []

        for event_type in EventType:
            qs = log_queryset.filter(event_type=event_type.value)
            graph = get_visualizations_graph(qs)

            totals.append([event_type.label, qs.count()])
            graphs.append([event_type.label, graph])

        return {'graphs': graphs, 'totals': totals, 'object': joboffer}

    def get(self, request, **kwargs):
        joboffer = self.get_object()

        context = self.get_context_data(joboffer)
        return render(request, self.template_name, context=context)


class DownloadAnalyticsAsCsv(JobOfferObjectMixin, View):
    model = JobOffer
    action_code = CODE_ANALYTICS

    def get(self, request, **kwargs):
        joboffer = self.get_object()

        data = get_visualization_data(joboffer)

        response = HttpResponse(content_type='text/csv')
        writer = csv.writer(response)

        writer.writerow([
          _('Fecha'), _('Hora'), _('ID. Oferta'), _('Titulo de la Oferta'), _('Código de Evento'),
          _('Evento')
        ])

        writer.writerows(data)
        return response


class JobOffersFeed(Feed):
    title = "Feed de ofertas laborales de Pyar"
    link = reverse_lazy("joboffers:list")

    def items(self):
        return JobOffer.objects.order_by('-created_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_pubdate(self, obj):
        return obj.created_at

    def item_link(self, item):
        return reverse('joboffers:view', args=[item.pk])

    def item_author_name(self, obj):
        return obj.company.name

    def item_author_email(self, obj):
        if obj.contact_mail:
            return obj.contact_mail
        else:
            return ''

    def item_author_link(self, obj):
        return obj.company.get_absolute_url()

    def item_categories(self, obj):
        return obj.tags.values_list('name', flat=True)
