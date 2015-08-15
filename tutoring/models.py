from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext as _
from django.db import models
from taggit.managers import TaggableManager


class Mentor(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name=_('Disponible'))
    start_date = models.DateTimeField(auto_now_add=True)
    slots = models.PositiveIntegerField(default=2, validators=[MaxValueValidator(4),
                                                               MinValueValidator(1)])
    tags = TaggableManager(verbose_name=_('Skills'))

    def __str__(self):
        return self.owner.username

    def get_absolute_url(self):
        return reverse('display_mentor', kwargs={'pk': self.pk})


class Apprentice(models.Model):
    STATUS_TRAINING = 'T'
    STATUS_IDLE = 'I'
    STATUS_WAITING = 'W'

    STATUS_CHOICES = (
        (STATUS_TRAINING, _('Entretenando')),
        (STATUS_IDLE, _('Inactivo')),
        (STATUS_WAITING, _('Buscando mentor')),
    )
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    description = models.TextField(blank=True, null=True, verbose_name=_('Descripción'))
    start_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_WAITING)

    tags = TaggableManager(verbose_name=_('Intereses'))

    def __str__(self):
        return self.owner.username

    def get_absolute_url(self):
        return reverse('display_apprentice', kwargs={'pk': self.pk})


class Project(models.Model):
    LOOKING_FOR_MENTOR = 'M'
    LOOKING_FOR_APPRENTICE = 'A'
    STATUS_OPEN = 'O'
    STATUS_IN_COURSE = 'I'
    STATUS_CLOSED = 'C'

    LOOKING_CHOICES = (
        (LOOKING_FOR_MENTOR, _('Buscando mentor')),
        (LOOKING_FOR_APPRENTICE, _('Buscando aprendiz')),
    )
    STATUS_CHOICES = (
        (STATUS_OPEN, _('Abierto')),
        (STATUS_IN_COURSE, _('En curso')),
        (STATUS_CLOSED, _('Cerrado')),
    )
    title = models.CharField(max_length=250, verbose_name=_('Título'))
    description = models.TextField(blank=True, verbose_name=_('Descripción'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_OPEN)
    link_repo = models.URLField(blank=True, verbose_name=_('URL del repositorio'))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    looking_for = models.CharField(max_length=1, choices=LOOKING_CHOICES, default=LOOKING_FOR_MENTOR)
    multiple_mentors = models.BooleanField(default=True, verbose_name=_('Múltiples mentores'))
    multiple_apprentices = models.BooleanField(default=True, verbose_name=_('Múltiples aprendices'))
    tags = TaggableManager()
    mentors = models.ManyToManyField(Mentor, blank=True)
    apprentices = models.ManyToManyField(Apprentice, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('display_project', kwargs={'pk': self.pk})


class Mentorship(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('Proyecto'))
    mentor = models.ForeignKey(Mentor, verbose_name=_('Mentor'))
    apprentice = models.ForeignKey(Apprentice, verbose_name=_('Aprendiz'))
    start_date = models.DateField(auto_now_add=True, verbose_name=_('Fecha de inicio'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('Fecha de finalización'))
    blog_link = models.URLField(blank=True, verbose_name=_('URL del blog'))

    def __str__(self):
        return '"{} - {} - {} - {}"'.format(self.project, self.mentor, self.apprentice, self.start_date)

    def get_absolute_url(self):
        return reverse('display_mentorship', kwargs={'pk': self.pk})
