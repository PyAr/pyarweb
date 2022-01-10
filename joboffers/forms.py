from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .models import JobOffer, JobOfferComment
from crispy_forms.layout import Submit, Reset, Layout
from crispy_forms.helper import FormHelper
from django_summernote.widgets import SummernoteInplaceWidget
from sanitizer.forms import SanitizedCharField

from jobs import utils


class JobOfferForm(forms.ModelForm):
    """A PyAr Jobs form."""

    description = SanitizedCharField(
        allowed_tags=settings.ALLOWED_HTML_TAGS_INPUT,
        allowed_attributes=settings.ALLOWED_HTML_ATTRIBUTES_INPUT,
        strip=False, widget=SummernoteInplaceWidget(), label='Descripción',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'company',
            'title',
            'location',
            'contact_mail',
            'contact_phone',
            'contact_url',
            'experience',
            'remoteness',
            'tags',
            'hiring_type',
            'salary',
            'description',
        )
        self.helper.attrs = {"novalidate": ""}

        self.helper.add_input(Submit('submit', _('Guardar')))
        self.helper.add_input(
            Reset('reset', _('Limpiar'), css_class='btn-default')
        )

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        self.cleaned_data['tags'] = utils.normalize_tags(tags)
        return self.cleaned_data['tags']

    class Meta:
        model = JobOffer
        exclude = ('created_by', 'modified_by', 'state', 'fields_hash')

        help_texts = {
            'company': 'Empresa que ofrece el trabajo',
            'title': 'Título del empleo, por ejemplo: Backend Developer',
            'location': 'Lugar de trabajo (País, Región)',
            'contact_mail': 'E-Mail de contacto',
            'contact_phone': 'Teléfono de contacto',
            'contact_url': 'URL de contacto (perfil de linkedin, facebook, sitio web, etc.)',
            'experience': 'Años de experiencia',
            'remoteness': 'Nivel de prescencialidad requerida.',
            'tags': 'Agregue algunos tags / etiquetas '
                    'que esten relacionadas con el puesto de trabajo. '
                    'Los tags deben estar separados por comas, por ejemplo: '
                    'Django, Python, MySQL, Linux',
            'hiring_type': 'Relación contractual con la empresa contratante.',
            'salary': 'Ej: 2000-3000 USD mensuales.',
            'description': 'Descripción de la oferta'
        }


class JobOfferCommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": ""}

        self.helper.add_input(Submit('submit', _('Guardar')))

    joboffer = forms.ModelChoiceField(queryset=JobOffer.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = JobOfferComment
        fields = ('joboffer', 'comment_type', 'text')
        labels = {
            'comment_type': _('Motivo de Rechazo'),
            'text': _('Comentario')
        }
