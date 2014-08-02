from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    """A PyAr events."""

    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100, verbose_name=_('Título'))
    description = models.TextField(verbose_name=_('Descripcion'))
    place = models.CharField(max_length=100, verbose_name=_('Lugar'))
    lat = models.CharField(max_length=20)
    lng = models.CharField(max_length=20)
    address = models.CharField(max_length=100, verbose_name=_('Direccion'))
    url = models.URLField()
    start_at = models.DateTimeField(verbose_name=_('Comienza a las'))
    end_at = models.DateTimeField(verbose_name=_('Termina a las'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s by %s" % (self.name, self.owner)
