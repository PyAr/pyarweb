from dal import autocomplete
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .models import JobOffer
from crispy_forms.layout import Submit, Reset, Layout
from crispy_forms.helper import FormHelper
from django_summernote.widgets import SummernoteInplaceWidget
from sanitizer.forms import SanitizedCharField
from taggit.models import Tag


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
            'hiring_type': '',
            'salary': '',
            'description': 'Descripción de la oferta'
        }


class TagSearchSelect2(autocomplete.Select2):
    """
    Custom version of Select2 autocomplete.

    It adds some js logic to autocomplete with tags and append them to the TagListWidget.
    It also fixes the .choices to load the current search value.
    """
    autocomplete_function = 'tag_search_select2'

    def get_context(self, name, value, attrs=None):
        """
        If there is a value, it add is to the choices list so it can be rendered approietly
        """
        if value:
            self.choices.append((value, value))

        return super().get_context(name, value, attrs)

    class Media:
        css = {'screen': ('css/select2-bootstrap.min.css',)}
        js = ('js/select2-bootstrap-theme.js',)


class TagListWidget(forms.CheckboxSelectMultiple):
    """
    Renders a list of values as checkboxes with boostrap's label style
    """
    template_name = 'joboffers/widgets/tag_list.html'


class SearchForm(forms.Form):
    """
    Form to validate search by text and tags.
    """
    q = forms.ChoiceField(
        widget=TagSearchSelect2(url='joboffers:tags-autocomplete')
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=TagListWidget()
    )

    class Media:
        js = ('js/joboffers/search-form.js',)
