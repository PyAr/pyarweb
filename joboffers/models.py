from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.urls import reverse
from taggit_autosuggest.managers import TaggableManager


class Experience(models.TextChoices):
    """
    Choices for JobOffer Experience.
    """
    ZERO = '0', _('0')
    ONE_PLUS = '1+', _('1+')
    TWO_PLUS = '2+', _('2+')
    THREE_PLUS = '3+', _('3+')
    FIVE_PLUS = '5+', _('5+')
    TEN_PLUS = '10+', _('10+')


class Remoteness(models.TextChoices):
    """
    Choices for Remoteness.
    """
    REMOTE = 'REMOTE', _('Remoto')
    OFFICE = 'IN_OFFICE', _('Presencial')
    HYBRID = 'MIXED', _('Mixto')


class HiringType(models.TextChoices):
    """
    Choices for HiringType.
    """
    EMPLOYEE = 'EMPLOYEE', _('Relación de dependencia')
    MONOTRIBUTISTA = 'MONOTRIBUTO', _('Monotributista')
    CONTRACTOR_SHORT = 'CONTRACTOR_SHORT', _('Contractor short term')
    CONTRACTOR_LONG = 'CONTRACTOR_LONG', _('Contractor long term')
    COOPERATIVE = 'COOPERATIVE', _('Cooperativa de trabajo')
    GOVERNMENT = 'GOVERNMENT', _('Estado')
    OTHER = 'OTHER', _('Otra')


class OfferState(models.TextChoices):
    """
    Choices for JobOfferStates.
    """
    NEW = 'NEW', _('Nuevo')  # Used only for actions
    DEACTIVATED = 'DEACTIVATED', _('Desactivada')
    MODERATION = 'MODERATION', _('En moderación')
    ACTIVE = 'ACTIVE', _('Activa')
    REJECTED = 'REJECTED', _('Rechazada')
    EXPIRED = 'EXPIRED', _('Caducada')


class JobOffer(models.Model):
    """A PyAr Job Offer."""

    title = models.CharField(max_length=255, verbose_name=_('Título'))
    company = models.ForeignKey(
        'pycompanies.Company',
        null=True,
        blank=True,
        verbose_name=_('Empresa'),
        on_delete=models.CASCADE,
    )
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Lugar'))
    contact_mail = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('E-mail')
    )
    contact_phone = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('Teléfono')
    )
    contact_url = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('Sitio web')
    )
    experience = models.CharField(
        max_length=3, choices=Experience.choices, verbose_name=_('Experiencia')
    )
    remoteness = models.CharField(
        max_length=32, choices=Remoteness.choices, verbose_name=_('Modalidad de trabajo')
    )
    tags = TaggableManager(verbose_name=_('Etiquetas'), blank=True)
    hiring_type = models.CharField(
        max_length=32, choices=HiringType.choices, verbose_name=_('Tipo de contratación')
    )
    salary = models.CharField(
        max_length=255, null=True, verbose_name=_('Rango salarial')
    )
    description = models.TextField(verbose_name=_('Descripción'))
    short_description = models.TextField(
        max_length=200,
        verbose_name=_('Descripción corta')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Rango salarial')
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Creado por'),
        related_name='created_offers',
    )
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Modificado por'),
        related_name='modified_offers',
    )
    state = models.CharField(
        max_length=32, choices=OfferState.choices, default=OfferState.DEACTIVATED,
        verbose_name=_('Estado de la oferta')
    )
    slug = AutoSlugField(populate_from='title', unique=True)
    fields_hash = models.CharField(
        max_length=255, null=True, verbose_name=_('Hash de la oferta')
    )

    def get_absolute_url(self):
        return reverse('joboffers:view', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_not_all_contact_info_null',
                check=(
                    models.Q(
                        contact_mail__isnull=False,
                    )
                    | models.Q(
                        contact_phone__isnull=False,
                    )
                    | models.Q(
                        contact_url__isnull=False,
                    )
                ),
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_location_not_null_when_not_remote',
                check=(
                    (
                        models.Q(remoteness__in=(Remoteness.HYBRID, Remoteness.OFFICE))
                        & models.Q(location__isnull=False)
                    )
                    | models.Q(remoteness=Remoteness.REMOTE)
                ),
            ),
        ]


class CommentType(models.TextChoices):
    """
    Choices for Types of JobOfferComments.
    """
    MODERATION = 'MODERATION', _('Moderación')
    EDITION = 'EDITION', _('Edición')
    SPAM = 'SPAM', _('Spam')
    INSUFICIENT = 'INSUFICIENT', _('Información insuficiente')
    NOT_RELATED = 'NOT_PYTHON', _('Oferta no relacionada con Python')


class JobOfferComment(models.Model):
    """
    A comment on a JobOffer.
    """
    text = models.TextField(verbose_name=_('Texto'))
    comment_type = models.CharField(
        max_length=32, choices=CommentType.choices, verbose_name=_('Tipo'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Rango salarial')
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Creado por'),
        related_name='created_joboffer_comments',
    )
    joboffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.joboffer.title}: {self.get_comment_type_display()}"
