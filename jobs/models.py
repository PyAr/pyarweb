from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from taggit_autosuggest.managers import TaggableManager
from pycompanies.models import Company

# Create your models here.


class Job(models.Model):

    """A PyAr Job."""

    title = models.CharField(max_length=255, verbose_name=_('Título'))
    company = models.ForeignKey(Company, null=True, blank=True,
                                verbose_name=_('Empresa'))
    description = models.TextField(verbose_name=_('Descripción'))
    location = models.CharField(max_length=100, verbose_name=_('Lugar'))
    email = models.EmailField()
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager(verbose_name=_('Etiquetas'))

    def __str__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return "/jobs/%i/" % self.id
