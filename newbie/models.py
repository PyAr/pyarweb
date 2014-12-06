from django.contrib.sites.models import Site
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.db import models
from taggit.managers import TaggableManager
from urllib.parse import urljoin

REQUEST_YES = "si"
REQUEST_NO = "no"
REQUEST_SUBJECT = "Hola, alguien quiere que le ensenes"
REQUEST_BODY = """
Hola alguien pregunta si podes ensenarle algunas cosas
Si puedo => %(yes_link)s

No puedo => %(no_link)s
"""

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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner')

    tags = TaggableManager()

    def __str__(self):
        return self.title


class Jedi(models.Model):
    """ A Jedi can teach to a Padawan """

    SLOT_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )

    user =  models.OneToOneField(settings.AUTH_USER_MODEL)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True, verbose_name=_('Estoy deponible'))
    start_date = models.DateTimeField(auto_now_add=True)
    notifications_ignored = models.PositiveIntegerField(default=0)
    slots = models.PositiveIntegerField(choices=SLOT_CHOICES, default=3)

    skills = TaggableManager()

    def __str__(self):
        return self.user.username


    def accept_padawan(self, padawan_id):
        """ A jedi can accept a Padawan """

        padawan = get_object_or_404(Padawan, id=padawan_id)
        project = Project.objects.create(
            title="Aprendiendo",
            created_by=self.user
        )
        project.padawan.add(padawan)
        project.jedi.add(self)
        project.save()
        self.slots -= 1
        self.save()


    def decline_project(self):
        """ A Jedi can reject a Project """
        pass


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
    description = models.TextField(blank=True, verbose_name=_('Descripción'))
    start_date = models.DateTimeField(auto_now_add=True)
    notifications_ignored = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=PADAWAN_STATUS_CHOICES, default=WAITING)

    interests = TaggableManager()

    def __str__(self):
        return self.user.username

    def send_project_request(self, jedi):
        """ Start the process for connect with a Jedi with by email """
        site = Site.objects.get(id=settings.SITE_ID)
        request_body = REQUEST_BODY  % {
            "yes_link": urljoin('//' + site.domain, reverse('jedi.answer', args=(self.id, jedi.id, REQUEST_YES))),
            "no_link":  urljoin('//' + site.domain, reverse('jedi.answer', args=(self.id, jedi.id, REQUEST_NO))),
        }
        send_mail(REQUEST_SUBJECT, request_body, self.user.email, [jedi.user.email])

    def folder_project(self):
        """ A Padawan can get out of a Porject """
        pass
