import html
import json
import re

from datetime import date

from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator
from django.db.models.aggregates import Count
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext as _

from easyaudit.models import CRUDEvent
from taggit_autosuggest.managers import TaggableManager

from pycompanies.models import UserCompanyProfile
from .constants import STATE_LABEL_CLASSES


class EventType(models.IntegerChoices):
    """
    Types of event visualization
    """
    LISTING_VIEW = (0, _('Visualización en Listado'))
    DETAIL_VIEW = (1, _('Visualización de la oferta completa'))
    CONTACT_INFO_VIEW = (2, _('Apertura de la información de contacto'))


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

    title = models.CharField(
      max_length=255, verbose_name=_('Título'), validators=[MinLengthValidator(20)], unique=True
    )
    company = models.ForeignKey(
        'pycompanies.Company',
        verbose_name=_('Empresa'),
        on_delete=models.CASCADE,
    )
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Lugar'))
    contact_mail = models.EmailField(
        max_length=255, blank=True, null=True, verbose_name=_('E-mail')
    )
    contact_phone = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('Teléfono')
    )
    contact_url = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('URL Contacto')
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
        max_length=512,
        verbose_name=_('Descripción corta')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Hora de creación')
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Creado por'),
        related_name='created_offers',
    )
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_('Hora de Modificación'))
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

    def get_absolute_url(self):
        url = reverse('joboffers:view', kwargs={'slug': self.slug})
        absolute_url = "".join((settings.BASE_URL, url))
        return absolute_url

    def __str__(self):
        return self.title

    @property
    def last_comment(self):
        """
        Return the last rejection JobOfferComment
        """
        return self.joboffercomment_set.last()

    @classmethod
    def get_short_description(cls, description):
        """
        Deduce the short_description from a given html description string
        """
        description_stripped_tags = re.sub(r'<[^>]*>', ' ', description)
        description_without_spaces = re.sub(r'\s+', ' ', description_stripped_tags).strip()
        description_unescaped = html.unescape(description_without_spaces)
        return description_unescaped[:512]

    def track_visualization(self, session, event_type: EventType):
        """
        Either get or create the matching JobOfferAccessLog instance for the joboffer.
        """
        today = date.today()
        month_year = today.year * 100 + today.month

        if session.session_key is None:
            session.save()

        return JobOfferAccessLog.objects.get_or_create(
            month_and_year=month_year,
            event_type=event_type,
            session=session.session_key,
            joboffer=self
        )

    def get_publisher_mail_addresses(self):
        """
        Return a list of the email addresses of the publishers of this offer.
        It filters users with empty mail field
        """
        profiles = UserCompanyProfile.objects.filter(company=self.company)

        addresses = set()
        for profile in profiles:
            if profile.user.email:
                addresses.add(profile.user.email)

        return addresses

    def get_visualizations_count(self):
        """
        Get a dict with visualizations count for every kind of event
        """
        items = JobOfferAccessLog.objects \
                                 .filter(joboffer=self) \
                                 .values_list('event_type') \
                                 .annotate(total=Count('event_type')) \
                                 .order_by()

        return dict(items)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.short_description:
            self.short_description = self.get_short_description(self.description)

        super().save(*args, **kwargs)

    @classmethod
    def get_options(cls):
        """
        Public _meta API accesor https://docs.djangoproject.com/en/4.0/ref/models/meta/
        """
        return cls._meta

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

    @classmethod
    def get_options(cls):
        """
        Public _meta API accesor https://docs.djangoproject.com/en/4.0/ref/models/meta/
        """
        return cls._meta

    def __str__(self):
        return f"{self.joboffer.title}: {self.get_comment_type_display()}"


class JobOfferHistoryManager(models.Manager):
    def for_offer(self, joboffer):
        """
        Get all the history objects for a given joboffer. It can be JobOffer and JobOfferComment
        """
        qs = super().get_queryset()

        offer_ctype = ContentType.objects.get(app_label='joboffers', model='joboffer')
        offer_comment_ctype = ContentType.objects.get(
            app_label='joboffers', model='joboffercomment'
        )

        offer_q = models.Q(event_type__lt=4, object_id=joboffer.id, content_type=offer_ctype)

        offer_comment_ids = [
            offer_comment.id for offer_comment in joboffer.joboffercomment_set.all()
        ]

        offer_comment_q = models.Q(
            object_id__in=offer_comment_ids, content_type=offer_comment_ctype
        )

        qs = qs.filter(offer_q | offer_comment_q)

        return qs


class JobOfferHistory(CRUDEvent):
    """
    This is a proxy model used to simplify the code take away all the logic from the controller
    """

    objects = JobOfferHistoryManager()

    @property
    def fields(self):
        """
        Return the representation of the joboffer after this particular change is applied.
        It returns a python dict that can contain different fields that the current model.
        """
        obj_repr = json.loads(self.object_json_repr)
        fields = obj_repr[0]['fields']
        return fields

    @property
    def joboffer_comment(self):
        """
        Return the JobOfferComment instance for the matching JobOfferHistory
        """
        if self.content_type.model != 'joboffercomment':
            raise ValueError("Unexpected model. Expected a JobOfferComment instance.")

        return JobOfferComment.objects.get(id=self.object_id)

    @property
    def changes(self):
        """
        Get a dict with the changes made to the object.
        """
        if self.changed_fields:
            return json.loads(self.changed_fields)
        else:
            return None

    @property
    def state_label(self):
        """
        Get the state of the joboffer at the time of the change
        """
        if self.content_type.model != 'joboffer':
            raise ValueError("Unexpected model. Expected a JobOffer instance.")

        fields = self.fields
        joboffer = JobOffer(state=fields['state'])
        return joboffer.get_state_display()

    @property
    def state_label_class(self):
        """
        Get the bootstrap label class for the matching joboffer state. Returns a default if the
        'state' field is not present. Maybe because a name update in the model.
        """
        if self.content_type.model != 'joboffer':
            raise ValueError("Unexpected model. Expected a JobOffer instance.")

        state = self.fields['state']

        return STATE_LABEL_CLASSES[state]

    class Meta:
        proxy = True


class JobOfferAccessLog(models.Model):
    """
    Model to track visualization of joboffers
    """
    created_at = models.DateTimeField(default=now)
    month_and_year = models.PositiveIntegerField()
    event_type = models.PositiveSmallIntegerField(
        choices=EventType.choices, verbose_name=_('Tipo de Evento')
    )
    session = models.CharField(max_length=40, verbose_name=_('Identificador de Sesión'))
    joboffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']
