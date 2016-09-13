from captcha.fields import CaptchaField
from django import forms
from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.translation import ugettext_lazy as _

from bootstrap3_datetime.widgets import DateTimePicker
from .models import Event, EventParticipation
from .mixins import CrispyFormMixin, ReadOnlyFieldsMixin


class EventForm(CrispyFormMixin):

    description = forms.CharField(widget=SummernoteInplaceWidget())

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

    class Meta(CrispyFormMixin.Meta):
        model = Event
        fields = (
            'name',
            'description',
            'place',
            'address',
            'url',
            'start_at',
            'end_at',
            'registration_enabled'
        )
        crispy_fields = fields
        help_texts = {
            'registration_enabled': _('Esta opción habilita la posiblidad de que la gente se '
                                      'inscriba al evento'),
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

    class Meta(CrispyFormMixin.Meta):
        model = EventParticipation
        fields = (
            'name',
            'email',
            'interest',
            'seniority',
            'captcha',
        )
        crispy_fields = fields


class AuthenticatedEventParticipationForm(ReadOnlyFieldsMixin, AnonymousEventParticipationForm):
    readonly_fields = ('name', 'email')
