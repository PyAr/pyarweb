# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import EventForm
from .models import Event
from .mixins import (
    LoginRequiredMixin,
    EventMixin,
    EventPermission
)


class EventList(ListView):
    queryset = Event.objects.order_by('-updated_at')
    paginate_by = 5


class EventDetail(EventMixin, DetailView):
    context_object_name = "event"


class EventCreate(LoginRequiredMixin, EventMixin, CreateView):
    form_class = EventForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(EventCreate, self).form_valid(form)


class EventUpdate(LoginRequiredMixin, EventPermission, UpdateView):
    form_class = EventForm

    def get_initial(self):
        event = self.get_object()

        return {'lat': event.lat, 'lng': event.lng}


class EventDelete(LoginRequiredMixin, EventPermission, DeleteView):
    pass
