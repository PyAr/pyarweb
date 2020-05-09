from random import choice
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from .models import Job, JobInactivated
from crispy_forms.layout import Submit, Reset, Layout
from crispy_forms.helper import FormHelper
from django_summernote.widgets import SummernoteInplaceWidget
from sanitizer.forms import SanitizedCharField

from jobs import utils


class JobForm(forms.ModelForm):
    """A PyAr Jobs form."""

    description = SanitizedCharField(
        allowed_tags=settings.ALLOWED_HTML_TAGS_INPUT,
        allowed_attributes=settings.ALLOWED_HTML_ATTRIBUTES_INPUT,
        strip=False, widget=SummernoteInplaceWidget())

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        company_help_text = ''.join((
            'Opcionalmente elija la empresa que ofrece el puesto. ',
            'Si la empresa no aparece en el listado, puede registrarla ',
            'haciendo click {0}'.format(
                '<a href="{0}">aquí</a>'
            ).format(
                reverse('companies:add')
            )))
        title_help_text = ''.join((
            'Título del empleo, por ejemplo: {0}'.format(
                choice([
                    'Backend Developer',
                    'Django Developer',
                    'Frontend Developer',
                    'Senior Django Developer',
                    'Full Stack Python Developer',
                ])
            )
        ))
        tags_help_text = ''.join((
            'Agregue algunos tags / etiquetas ',
            'que esten relacionadas con el puesto de trabajo. '
            'Los tags deben estar separados por comas, por ejemplo: ',
            'Django, Python, MySQL, Linux'
        ))

        seniority_help_text = ''.join((
            'Opcionalmente puede especificar la experiencia requerida ',
            'para el puesto.'
        ))

        remote_work_help_text = ''.join((
            'Se permite la modalidad de trabajo desde casa (homeworking).'
        ))

        self.fields['title'].label = 'Título de la oferta'
        self.fields['tags'].label = 'Etiquetas / Tags / Tecnologías'
        self.fields['title'].help_text = title_help_text
        self.fields['tags'].help_text = tags_help_text
        self.fields['seniority'].help_text = seniority_help_text
        self.fields['company'].help_text = company_help_text
        self.fields['remote_work'].help_text = remote_work_help_text
        self.fields['description'].label = 'Descripción'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'company',
            'location',
            'email',
            'seniority',
            'remote_work',
            'tags',
            'description',
        )
        self.helper.add_input(Submit('job_submit', _('Guardar')))
        self.helper.add_input(Reset('job_reset', _('Limpiar'),
                                    css_class='btn-default'))

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        self.cleaned_data['tags'] = utils.normalize_tags(tags)
        return self.cleaned_data['tags']

    class Meta:
        model = Job
        exclude = ('owner', 'is_active')


class JobInactivateForm(forms.ModelForm):
    """ Form to inactivate Job  """

    send_email = forms.BooleanField(label='¿Enviar mail al dueño del aviso?',
                                    required=False)

    def __init__(self, *args, **kwargs):
        super(JobInactivateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'reason',
            'comment',
            'send_email',
        )

        self.helper.add_input(Submit('job_inactivate_submit', _('Guardar')))
        self.helper.add_input(Reset('job_inactivate_reset', _('Limpiar'),
                                    css_class='btn-default'))

    class Meta:
        model = JobInactivated
        exclude = ('job', )
