from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from autoslug import AutoSlugField

from jobs.models import JOB_SENIORITIES


GENDER_OPTIONS = (
    ('female', _('femenino')),
    ('male', _('masculino')),
    ('Otro', _('otro')),
)


class Event(models.Model):
    """A PyAr events."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_('Título'))
    description = models.TextField(verbose_name=_('Descripcion'))
    place = models.CharField(max_length=100, verbose_name=_('Lugar'))
    address = models.CharField(max_length=100, verbose_name=_('Direccion'))
    slug = AutoSlugField(
        editable=True, null=True, blank=True, unique=True, populate_from='name',
    )
    url = models.URLField(blank=True, null=True)
    start_at = models.DateTimeField(verbose_name=_('Comienza a las'))
    end_at = models.DateTimeField(verbose_name=_('Termina a las'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registration_enabled = models.BooleanField(default=False,
                                               verbose_name=_('¿Habilitar inscripción'))
    has_sponsors = models.BooleanField(default=False, verbose_name=_('¿El evento tiene sponsors?'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('events:detail', args=[self.id])


class EventParticipation(models.Model):
    """A registration record to a PyAr event."""

    event = models.ForeignKey(Event, related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_('nombre, nick, alias...'))
    email = models.EmailField(max_length=255, verbose_name=_('email'))
    interest = models.TextField(verbose_name=_('intereses'), blank=True)

    seniority = models.CharField(
        max_length=100,
        blank=True,
        default='',
        choices=JOB_SENIORITIES + (('guido', _('Soy Guido Van Rossum')),),
        verbose_name=_('experiencia')
    )

    gender = models.CharField(
        max_length=32,
        blank=True,
        default='',
        choices=GENDER_OPTIONS,
        verbose_name=_('género')
    )

    cv = models.URLField(max_length=1024, blank=True, default='', verbose_name='curriculum vitae')
    share_with_sponsors = models.BooleanField(
        default=False, verbose_name=_('¿Querés compartir tus datos con los sponsors?'))
    confirmed = models.BooleanField(
        default=False,
        verbose_name=_('Participación confirmada')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("event", "email")

    def __str__(self):
        result = "Inscripción de %s" % self.name
        if self.event:
            result += " a %s" % self.event.name
        return result

    @property
    def is_verified(self):
        """An EventParticipation in confirmed if the user is registered."""
        is_a_pyar_user = self.user is not None
        return is_a_pyar_user
