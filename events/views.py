from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)
from braces.views import LoginRequiredMixin

from community.views import OwnedObject

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
    success_message = "Participation successfully registered. <b>hey</>"

    def form_valid(self, form):
        # If user is authenticated, then set instance.owner, else dont worry
        form.instance.event_id = self.kwargs['pk']
        return super(EventParticipationCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('events:detail', kwargs=self.kwargs)
