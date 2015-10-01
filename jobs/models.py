from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from pycompanies.models import Company
from taggit_autosuggest.managers import TaggableManager
from model_utils.models import TimeStampedModel

JOB_SENIORITIES = (
    ('Trainee', 'Trainee'),
    ('Junior', 'Junior'),
    ('Semi Senior', 'Semi Senior'),
    ('Senior', 'Senior'),
)


class JobManager(models.Manager):
    def get_query_set(self):
        # -- only active jobs
        return super(JobManager, self).get_query_set().filter(is_active=True)


class Job(models.Model):
    """A PyAr Job."""

    title = models.CharField(max_length=255, verbose_name=_('Título'))
    company = models.ForeignKey(Company,
                                null=True,
                                blank=True,
                                verbose_name=_('Empresa'))
    description = models.TextField(verbose_name=_('Descripción'))
    location = models.CharField(max_length=100, verbose_name=_('Lugar'))
    email = models.EmailField()
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager(verbose_name=_('Etiquetas'))
    remote_work = models.BooleanField(
        default=False,
        verbose_name=_('Trabajo Remoto'))
    seniority = models.CharField(
        max_length=100,
        blank=True,
        default='',
        choices=JOB_SENIORITIES,
        verbose_name=_('Experiencia'))
    slug = AutoSlugField(populate_from='title', unique=True)
    is_active = models.BooleanField(default=True)

    objects = JobManager()

    def __str__(self):
        return u'{0}'.format(self.title)

    @property
    def is_remote_work_allowed(self):
        return self.remote_work

    def get_absolute_url(self):
        return reverse('jobs_view', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created']


class JobInactivated(TimeStampedModel):
    """ Jobs Inactivated """
    REASONS = (
        ('No es un aviso relacionado con Python', 'No es un aviso relacionado con Python'),
        ('Spam', 'Spam'),
    )

    job = models.ForeignKey(Job)
    reason = models.CharField(
        max_length=100,
        blank=False,
        choices=REASONS,
        verbose_name=_('Motivo/Razón'))
    comment = models.TextField(blank=True, null=True, verbose_name=_('Comentario'))
