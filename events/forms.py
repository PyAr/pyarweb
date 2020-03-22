from captcha.fields import CaptchaField
from crispy_forms.layout import Field
from django import forms
from django.conf import settings
from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.translation import ugettext_lazy as _

from bootstrap3_datetime.widgets import DateTimePicker
from sanitizer.forms import SanitizedCharField

from .models import Event, EventParticipation
from .mixins import CrispyFormMixin, ReadOnlyFieldsMixin


REGISTRATION_ENABLED_HELP_TEXT = _(
    'Esta opción habilita la posiblidad de que la gente se inscriba al evento')
HAS_SPONSORS_HELP_TEXT = _(
    'Si se marca esta opción, y se habilitan las inscripciones, entonces se le consultará a los '
    'inscriptos si quieren compartir sus datos con los sponsors y se les dará la opción de linkear'
    ' a un CV.')


class EventForm(CrispyFormMixin):

    description = SanitizedCharField(
        allowed_tags=settings.ALLOWED_HTML_TAGS_INPUT,
        allowed_attributes=settings.ALLOWED_HTML_ATTRIBUTES_INPUT,
        allowed_styles=settings.ALLOWED_HTML_STYLES_INPUT,
        strip=False, widget=SummernoteInplaceWidget())

    start_at = forms.DateTimeField(
        required=True,
        input_formats=['%d/%m/%Y %H:%M:%S'],
        label=_('Comienza'),
        widget=DateTimePicker(
            options={
                "format": "DD/MM/YYYY HH:ss:mm"
            }
        )
    )

    end_at = forms.DateTimeField(
        required=True,
        input_formats=['%d/%m/%Y %H:%M:%S'],
        label=_('Finaliza'),
        widget=DateTimePicker(
            options={
                "format": "DD/MM/YYYY HH:ss:mm"
            }
        )
    )

    def get_crispy_fields(self):
        return self.Meta.fields

    class Meta:
        model = Event
        fields = (
            'name',
            'description',
            'place',
            'address',
            'slug',
            'url',
            'start_at',
            'end_at',
            'registration_enabled',
            'has_sponsors'
        )
        crispy_fields = fields
        help_texts = {
            'registration_enabled': REGISTRATION_ENABLED_HELP_TEXT,
            'has_sponsors': HAS_SPONSORS_HELP_TEXT,
        }

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        start_at = cleaned_data.get('start_at')
        end_at = cleaned_data.get('end_at')
        if start_at is not None and end_at is not None:
            if start_at > end_at:
                msg = 'La fecha de inicio es menor a la fecha de finalizacion'
                self._errors['start_at'] = [_(msg)]
                self._errors['end_at'] = [_(msg)]
        return cleaned_data

    def save(self, *args, **kwargs):
        super(EventForm, self).save(*args, **kwargs)
        self.instance.save()


class AnonymousEventParticipationForm(CrispyFormMixin):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        event = self.initial['event']
        if not event.has_sponsors:
            for field_name in ('cv', 'share_with_sponsors'):
                field_layout = self.helper[field_name]
                field_layout.wrap(Field, type="hidden")

    class Meta:
        model = EventParticipation
        fields = (
            'name',
            'email',
            'interest',
            'gender',
            'seniority',
            'share_with_sponsors',
            'cv',
            'captcha',
        )
        help_texts = {
            'interest': _('¿Qué temas de Python te interesaría ver en una charla?'),
            'gender':  _('Queremos reducir la brecha de género. Este dato nos ayuda.'),
            'cv': 'Dejanos un link a tu CV, perfil de LinkedIn o algo similar'
        }


class AuthenticatedEventParticipationForm(ReadOnlyFieldsMixin, AnonymousEventParticipationForm):
    # The authenticated user does not need to fill a captcha. That's why the field is marked as
    # read-only and not included in the fields list (so it won't render).
    readonly_fields = ('name', 'email', 'captcha',)

    class Meta(AnonymousEventParticipationForm.Meta):
        fields = (
            'name',
            'email',
            'interest',
            'gender',
            'seniority',
            'share_with_sponsors',
            'cv',
        )
