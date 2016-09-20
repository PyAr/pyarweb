from braces.views import LoginRequiredMixin
from community.views import validate_obj_owner, OwnedObject
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)

from .forms import EventForm, AnonymousEventParticipationForm, AuthenticatedEventParticipationForm
from .models import Event, EventParticipation
from .mixins import EventMixin, EventParticipationMixin, CSVResponseMixin


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

    def aux_get_user_name(self):
        user = self.request.user
        return user.get_full_name() or user.get_username()

    def form_valid(self, form):
        # Set the EventParticipation event from the URL param.
        event_id = self.kwargs['pk']
        form.instance.event_id = event_id

        if self.request.user.is_authenticated():
            response = self.form_valid_for_authenticated_user(form)
        else:
            response = self.form_valid_for_anonymous_user(form)

        return response

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        if self.request.user.is_authenticated():
            event = self.get_event()
            participation = event.participants.filter(user_id=self.request.user.id)
            if participation.exists():
                return HttpResponseRedirect(
                    reverse_lazy('events:registration',
                                 kwargs={'pk': event.id, 'participation_pk': participation.get().id})
                )
        return super().get(request, *args, **kwargs)


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
        initial['event'] = self.get_event()
        user = self.request.user
        if user.is_authenticated():
            initial['name'] = self.aux_get_user_name()
            initial['email'] = user.email
        return initial

    def get_success_message(self, cleaned_data):
        success_message = "Tu inscripción al evento ha sido registrada."
        if not self.request.user.is_authenticated():
            success_message = "Recibirás un email para confirmar la dirección provista y así " \
                              "completar tu inscripción."
        return _(success_message + '<br><i>¡Muchas gracias!</i>')

    def form_valid_for_authenticated_user(self, form):
        form.instance.user = self.request.user
        form.instance.name = self.aux_get_user_name()
        form.instance.email = self.request.user.email

        return super().form_valid(form)

    def form_valid_for_anonymous_user(self, form):
        if EventParticipation.objects.filter(email=form.instance.email).exists():
            # If the email is already registered, silently redirect to the success URL.
            # This is to avoid any information leaking.
            return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)


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

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        initial['event'] = self.get_event()
        return initial

    def get_success_url(self):
        return self.object.event.get_absolute_url()


class EventParticipationList(LoginRequiredMixin, ListView):
    http_method_names = [u'get']
    context_object_name = 'participants'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__event = None

    def get_context_data(self, **kwargs):
        """Overwrite get_context_data to add the related Event's ID to the template context."""
        context = super(EventParticipationList, self).get_context_data(**kwargs)
        context['event'] = self.event
        return context

    @property
    def event(self):
        if self.__event is None:
            event = Event.objects.get(pk=self.kwargs['pk'])
            self.__event = validate_obj_owner(event, self.request.user)
        return self.__event

    def get_queryset(self):
        self.queryset = self.event.participants.all()
        return super().get_queryset()


class EventParticipationDelete(LoginRequiredMixin, EventParticipationMixin, DeleteView):
    pk_url_kwarg = 'participation_pk'

    def get_object(self, *args, **kwargs):
        """A User can delete its participation to an Event. The Event owner can also do that."""

        inscription = super(EventParticipationDelete, self).get_object(*args, **kwargs)
        if self.request.user not in [inscription.user, inscription.event.owner]:
            raise Http404()
        return inscription


class EventParticipationDownload(CSVResponseMixin, EventParticipationList):
    def get_csv_filename(self):
        event = self.event.name.lower().replace(' ', '_')
        timestamp = timezone.now().isoformat().replace(':', '').replace('-', '').split('.')[0]
        return '{0}-{1}.csv'.format(event, timestamp)

    def get_rows(self):
        columns = ('Nombre', 'Correo electrónico', 'Nivel', 'Usuario PyAr', 'Verificado?')
        if self.event.has_sponsors:
            columns += ('CV', 'Comparte?')
        header = [columns]
        return header + list(map(self.participation_to_row, self.get_queryset()))

    def participation_to_row(self, obj):
        """Auxiliary method to convert an EventParticipation instance in a row for the CSV file."""
        user = ''
        if obj.user is not None:
            user = obj.user.get_full_name() or obj.user.get_username()
        row = (obj.name, obj.email, obj.seniority, user, obj.is_verified)
        if self.event.has_sponsors:
            row += (obj.cv, obj.share_with_sponsors)
        return row
