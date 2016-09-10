# -*- coding: utf-8 -*-

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Div, Field
from crispy_forms.helper import FormHelper
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from .models import Event


class EventMixin(object):
    """Mixin for common attrs."""

    model = Event

    def get_success_url(self):
        return reverse_lazy('events:events_list_all')



class CrispyFormMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_method = "post"
        self.helper.add_input(Submit('job_submit', _('Guardar')))
        self.helper.add_input(Reset('job_reset', _('Limpiar'),
                              css_class='btn-default'))
        self.helper.layout = Layout(
            Div(*self.Meta.crispy_fields)
        )


    class Meta:
        crispy_fields = []
