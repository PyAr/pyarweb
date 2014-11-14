# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy

from .models import Event


class EventMixin(object):
    """Mixin for common attrs."""

    model = Event

    def get_success_url(self):
        return reverse_lazy('events:events_list_all')
