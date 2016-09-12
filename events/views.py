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

from .forms import EventForm, EventParticipationForm
from .models import Event, EventParticipation
from .mixins import EventMixin

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


class EventParticipationCreate(SuccessMessageMixin, CreateView):
    model = EventParticipation
    form_class = EventParticipationForm
    success_message = _("Tu inscripción al evento ha sido registrada.<br><i>¡Muchas gracias!</i>")

    def form_valid(self, form):
        event_id = self.kwargs['pk']
        already_subscribed = EventParticipation.objects.filter(event_id=event_id,
                                                               email=form.instance.email).exists()
        if already_subscribed:
            form.add_error('email', ValidationError(_('Este email ya se inscripto en este evento')))
            return super(EventParticipationCreate, self).form_invalid(form)

        form.instance.event_id = event_id
        return super(EventParticipationCreate, self).form_valid(form)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        user = self.request.user
        if user.is_authenticated():
            initial['name'] = user.get_full_name() or user.get_username()
            initial['email'] = user.email
        return initial

    def get_success_url(self):
        return reverse('events:detail', kwargs=self.kwargs)


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
