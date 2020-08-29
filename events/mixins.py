# -*- coding: utf-8 -*-
import csv

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Div
from django import forms
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from .models import Event, EventParticipation


class CrispyFormMixin(forms.ModelForm):
    """Form with Guardar and Limpiar buttons, based in crispy forms."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_method = "post"
        self.helper.add_input(Submit('job_submit', _('Guardar')))
        self.helper.add_input(Reset('job_reset', _('Limpiar'),
                              css_class='btn-default'))
        self.helper.layout = Layout(
            Div(*self.get_crispy_fields())
        )

    def get_crispy_fields(self):
        return self.Meta.fields


class EventMixin(object):
    """Mixin for common attrs."""

    model = Event

    def get_success_url(self):
        return reverse_lazy('events:events_list_all')


class EventParticipationMixin(object):
    """Mixin for common attrs."""

    model = EventParticipation

    def get_event(self):
        event_id = self.kwargs['pk']
        return Event.objects.get(pk=event_id)

    def get_success_url(self):
        return reverse_lazy('events:detail', kwargs={'pk': self.kwargs['pk']})


class ReadOnlyFieldsMixin(object):
    """Adds the posibility to declare fields as read-only (until we update to Django 1.9 or so"""

    readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super(ReadOnlyFieldsMixin, self).__init__(*args, **kwargs)
        for field in (field for name, field in self.fields.items() if
                      name in self.readonly_fields):
            field.widget.attrs['disabled'] = 'true'
            field.required = False

    def clean(self):
        for f in self.readonly_fields:
            self.cleaned_data.pop(f, None)
        return super(ReadOnlyFieldsMixin, self).clean()


class CSVResponseMixin(object):
    """Return a csv file based on a list of lists."""
    csv_filename = 'csvfile.csv'

    def get(self, request, *args, **kwargs):
        return self.render_to_csv()

    def get_rows(self):
        raise NotImplementedError()

    def get_csv_filename(self):
        return self.csv_filename

    def render_to_csv(self):
        response = HttpResponse(content_type='text/csv')
        cd = 'attachment; filename="{0}"'.format(self.get_csv_filename())
        response['Content-Disposition'] = cd

        writer = csv.writer(response)
        for row in self.get_rows():
            writer.writerow(row)

        return response
