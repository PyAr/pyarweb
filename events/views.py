# -*- coding: utf-8 -*-

from django.shortcuts import render
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
    paginate_by = 10

class EventDetail(EventMixin, DetailView):
    context_object_name = "event"

class EventCreate(LoginRequiredMixin, EventMixin, CreateView):
    form_class = EventForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(EventCreate, self).form_valid(form)

class EventUpdate(LoginRequiredMixin, EventPermission, UpdateView):
    form_class = EventForm


class EventDelete(LoginRequiredMixin, EventPermission, DeleteView):
    pass