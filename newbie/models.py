from django.conf import settings
from django.utils.translation import ugettext as _
from django.db import models
from taggit.managers import TaggableManager


class Project(models.Model):
    """ A project which connect a Jedi with a Padawan """

    jedi = models.ManyToManyField("Jedi")
    padawan = models.ManyToManyField("Padawan")
    start_date = models.DateTimeField(auto_now_add=True, null=True)
    end_date = models.DateTimeField(null=True, blank=True)
    blog_link = models.URLField(blank=True, verbose_name=_('Blog link'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    link_repo = models.URLField(blank=True, verbose_name=_('Link repo'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    tags = TaggableManager()

    def __str__(self):
        return self.title


class Jedi(models.Model):
    """ A Jedi can teach to a Padawan """

    user =  models.OneToOneField(settings.AUTH_USER_MODEL)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True, verbose_name=_('Estoy deponible'))
    start_date = models.DateTimeField(auto_now_add=True)
    notifications_ignored = models.PositiveIntegerField(default=0)

    skills = TaggableManager()

    def __str__(self):
        return self.user.username


class Padawan(models.Model):
    """ A Padawan can be adopted by a Jedi """

    TRAINING = "TRAINING"
    IDLE = "IDLE"
    WAITING = "WAITING"

    PADAWAN_STATUS_CHOICES = (
        (TRAINING, "TRAINING"),
        (IDLE, "IDLE"),
        (WAITING, "WAITING"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    description = models.TextField(blank=True, verbose_name=_('Description'))
    start_date = models.DateTimeField(auto_now_add=True)
    notifications_ignored = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=PADAWAN_STATUS_CHOICES, default=WAITING)

    interests = TaggableManager()

    def __str__(self):
        return self.user.username
