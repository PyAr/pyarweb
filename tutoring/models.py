from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext as _
from django.db import models
from taggit.managers import TaggableManager


class Project(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('Título'))
    description = models.TextField(blank=True, verbose_name=_('Descripción'))
    link_repo = models.URLField(blank=True, verbose_name=_('URL del repositorio'))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    tags = TaggableManager()

    def __str__(self):
        return self.title


class Mentor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name=_('Disponible'))
    start_date = models.DateTimeField(auto_now_add=True)
    slots = models.PositiveIntegerField(default=2, validators=[MaxValueValidator(4),
                                                               MinValueValidator(1)])
    skills = TaggableManager(verbose_name=_('Skills'))

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('update_mentor', kwargs={'pk': self.id})


class Apprentice(models.Model):
    STATUS_TRAINING = 'T'
    STATUS_IDLE = 'I'
    STATUS_WAITING = 'W'

    STATUS_CHOICES = (
        (STATUS_TRAINING, _('Entretenando')),
        (STATUS_IDLE, _('Inactivo')),
        (STATUS_WAITING, _('Buscando mentor')),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    description = models.TextField(blank=True, null=True, verbose_name=_('Descripción'))
    start_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_WAITING)

    interests = TaggableManager(verbose_name=_('Intereses'))

    def __str__(self):
        return self.user.username


class Mentorship(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('Proyecto'))
    mentor = models.ForeignKey(Mentor, verbose_name=_('Mentor'))
    apprentice = models.ForeignKey(Apprentice, verbose_name=_('Aprendiz'))
    start_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de inicio'))
    end_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Fecha de finalización'))
    blog_link = models.URLField(blank=True, verbose_name=_('URL del blog'))
