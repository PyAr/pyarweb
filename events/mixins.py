# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator

from .models import Event

class LoginRequiredMixin(object):
    """Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class EventMixin(object):
    """Mixin for common attrs."""
    model = Event
    success_url = reverse_lazy('events:events_list_all')

class EventPermission(EventMixin, object):
    """Ensures that only the owner can edit or delete his events."""

    def get_object(self, queryset=None):
        """Hook to ensure object is owned by request.user."""
        event = super(EventPermission, self).get_object()
        if not event.owner == self.request.user:
            raise Http404
        return event