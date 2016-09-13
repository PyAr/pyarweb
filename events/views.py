from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)
from braces.views import LoginRequiredMixin

from community.views import validate_obj_owner, OwnedObject

from .forms import EventForm, AnonymousEventParticipationForm, AuthenticatedEventParticipationForm
from .models import Event, EventParticipation
from .mixins import EventMixin, EventParticipationMixin

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse, reverse_lazy


class EventsFeed(Feed):
    title = "Feed de Próximos Eventos de PyAr"
    link = reverse_lazy("events:events_list_all")
    description = "Eventos de Python Argentina y relacionados"
    description_template = "events/event_detail_body.html"

    def items(self):
        return Event.objects.filter(end_at__gte=timezone.now()).order_by('-updated_at')[:10]

    def item_title(self, item):
        return item.name

    def item_pubdate(self, item):
        return item.created_at

    def item_updateddate(self, item):
        return item.updated_at

    def author_name(self, item):
        if item:
            return str(item.owner)
        return ''


class EventList(ListView):
    queryset = Event.objects.filter(
        end_at__lt=timezone.now()).order_by('-start_at')
    paginate_by = 5
    context_object_name = "eventos_pasados"

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['eventos_proximos'] = Event.objects.filter(
            end_at__gte=timezone.now()).order_by('start_at')

        return context


class EventDetail(EventMixin, DetailView):
    context_object_name = "event"

    def user_participation_details(self):
        """
        Collect the necessary info for the template context if the user is already registered to the
        Event.
        :return: dict with 'user_is_registered' (bool) and  'participation_id' (int | None) fields

        """
        details = {
            'user_is_registered': False,
            'participation_id': None
        }
        user = self.request.user
        if user.is_anonymous():
            return details

        try:
            participation = self.object.participants.get(user=user)
            details.update(user_is_registered=True, participation_id=participation.id)
        except EventParticipation.DoesNotExist:
            pass
        return details

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context.update(self.user_participation_details())
        return context


class EventCreate(LoginRequiredMixin, EventMixin, CreateView):
    form_class = EventForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(EventCreate, self).form_valid(form)


class EventUpdate(LoginRequiredMixin, EventMixin, OwnedObject, UpdateView):
    form_class = EventForm


class EventDelete(LoginRequiredMixin, OwnedObject, DeleteView):
    model = Event
    success_url = reverse_lazy("events:events_list_all")


class EventParticipationCreate(SuccessMessageMixin, EventParticipationMixin, CreateView):
    form_class = AnonymousEventParticipationForm
    success_message = _("Tu inscripción al evento ha sido registrada.<br><i>¡Muchas gracias!</i>")

    def aux_get_user_name(self):
        user = self.request.user
        return user.get_full_name() or user.get_username()

    def form_valid(self, form):
        event_id = self.kwargs['pk']
        inscription = form.instance
        inscription.event_id = event_id

        user = self.request.user
        if user.is_authenticated():
            inscription.user = user
            inscription.name = self.aux_get_user_name()
            inscription.email = user.email
        else:
            # send validation email
            pass

        return super(EventParticipationCreate, self).form_valid(form)

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        self.form_class = AnonymousEventParticipationForm
        if self.request.user.is_authenticated():
            self.form_class = AuthenticatedEventParticipationForm
        return self.form_class

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        user = self.request.user
        if user.is_authenticated():
            initial['name'] = self.aux_get_user_name()
            initial['email'] = user.email
        return initial


class EventParticipationDetail(LoginRequiredMixin, SuccessMessageMixin, EventParticipationMixin,
                               UpdateView):
    pk_url_kwarg = 'participation_pk'
    success_message = _("Tu inscripción al evento ha sido actualizada.")

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        self.form_class = AnonymousEventParticipationForm
        if self.request.user.is_authenticated():
            self.form_class = AuthenticatedEventParticipationForm
        return self.form_class

    def get_success_url(self):
        return self.object.event.get_absolute_url()


class EventParticipationList(LoginRequiredMixin, ListView):
    http_method_names = [u'get']
    context_object_name = 'participants'

    def get_context_data(self, **kwargs):
        """Overwrite get_context_data to add the related Event's ID to the template context."""
        context = super(EventParticipationList, self).get_context_data(**kwargs)
        context['event'] = self.event
        return context

    def get_event(self):
        event = Event.objects.get(pk=self.kwargs['pk'])
        self.event = validate_obj_owner(event, self.request.user)
        return self.event

    def get_queryset(self):
        event = self.get_event()
        self.queryset = event.participants.all()
        return super().get_queryset()


class EventParticipationDelete(LoginRequiredMixin, OwnedObject, EventParticipationMixin,
                               DeleteView):
    pk_url_kwarg = 'participation_pk'
