from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)

from braces.views import LoginRequiredMixin

from community.views import OwnedObject

from .forms import EventForm
from .models import Event
from .mixins import EventMixin


class EventList(ListView):
    queryset = Event.objects.filter(
        end_at__lt=timezone.now()).order_by('-updated_at')
    paginate_by = 5
    context_object_name = "eventos_pasados"

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['eventos_proximos'] = Event.objects.filter(
            end_at__gte=timezone.now()).order_by('-updated_at')

        return context


class EventDetail(EventMixin, DetailView):
    context_object_name = "event"


class EventCreate(LoginRequiredMixin, EventMixin, CreateView):
    form_class = EventForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(EventCreate, self).form_valid(form)

    def get_initial(self):
        return {'lat': '-35.245619', 'lng': '-65.492249'}


class EventUpdate(LoginRequiredMixin, EventMixin, OwnedObject, UpdateView):
    form_class = EventForm

    def get_initial(self):
        event = self.get_object()

        return {'lat': event.lat, 'lng': event.lng, 'zoom': event.zoom}


class EventDelete(LoginRequiredMixin, OwnedObject, DeleteView):
    model = Event
    success_url = '/events/'
