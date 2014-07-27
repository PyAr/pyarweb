from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Job
from crispy_forms.layout import Submit, Reset, Layout, Div, Field
from crispy_forms.helper import FormHelper
from django_summernote.widgets import SummernoteInplaceWidget


class JobForm(forms.ModelForm):
    """A PyAr Jobs form."""
    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('job_submit', _('Submit')))
        self.helper.add_input(Reset('job_reset', _('Reset'), css_class='btn-default'))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Div(
                'title',
                'company',
                'location',
                css_class='col-md-6'
            ),
            Div(
                'email',
                'tags',
                css_class='column col-md-6'
            ),
            Div(
            	'description',
            	css_class='column col-md-12'
            ),
        )

    class Meta:
        model = Job
        exclude = ('owner',)
