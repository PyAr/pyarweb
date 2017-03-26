from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from email_confirm_la.models import EmailConfirmation

from jobs.models import JOB_SENIORITIES


class Event(models.Model):
    """A PyAr events."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100, verbose_name=_('Título'))
    description = models.TextField(verbose_name=_('Descripcion'))
    place = models.CharField(max_length=100, verbose_name=_('Lugar'))
    address = models.CharField(max_length=100, verbose_name=_('Direccion'))
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

    event = models.ForeignKey(Event, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
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
    cv = models.URLField(max_length=1024, blank=True, default='', verbose_name='curriculum vitae')
    share_with_sponsors = models.BooleanField(
        default=False, verbose_name=_('¿Querés compartir tus datos con los sponsors?'))
    confirmed = models.BooleanField(
        default=False,
        verbose_name=_('Participación confirmada')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_confirmations = GenericRelation('email_confirm_la.EmailConfirmation',
                                          content_type_field='content_type',
                                          object_id_field='object_id')

    class Meta:
        unique_together = ("event", "email")

    def __str__(self):
        result = "Inscripción de %s" % self.name
        if self.event:
            result += " a %s" % self.event.name
        return _(result)

    def verify_email(self):
        """Start the email-verification process with this instance's email attribute."""

        EmailConfirmation.objects.verify_email_for_object(
            email=self.email,
            content_object=self,
            email_field_name='email'
        )

    @property
    def is_verified(self):
        is_a_pyar_user = self.user is not None
        email_was_verified = not self.email_confirmations.exists()
        return is_a_pyar_user or email_was_verified


@receiver(post_save, sender=EventParticipation)
def post_anonymous_participation_creation(sender, instance, created, **kwargs):
    """After an EventParticipation is created, if it's anonymous (not a PyAr user), start the
       email-verification process.
    """
    if created and instance.user is None:
        instance.verify_email()

