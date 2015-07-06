from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from taggit_autosuggest.managers import TaggableManager
from model_utils.models import TimeStampedModel
from cities_light.models import City


class Profiles(TimeStampedModel):
    """
    Perfiles de usuarios
    """
    user = models.OneToOneField(User)
    tutor = models.BooleanField(verbose_name=_("Querés enseñar?"),
                                default=False)
    tutorado = models.BooleanField(verbose_name=_("Querés recibir ayuda de un tutor?"),
                                   default=False)
    disponibilidad_semanal = models.IntegerField(verbose_name=_("Cantidad de horas semanales"))
    intereses = TaggableManager(verbose_name=_('Que temas te interesan?'), blank=True)
    ciudad = models.ForeignKey("cities_light.City")

    class Meta:
        ordering = ['-created']


class MediosContactos(TimeStampedModel):
    """
    Medios de contactos, ejemplo: Skype, Facebook, Email, etc
    """
    nombre = models.CharField(blank=False, max_length=150)

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return u'{0}'.format(self.nombre)

    class Meta:
        ordering = ['-created']


class ProfilesMediosContactos(TimeStampedModel):
    """
    Relacion perfiles con medios de contactos
    """
    profile = models.ForeignKey(Profiles)
    medio_contacto = models.ForeignKey(MediosContactos, verbose_name=_("Medio de contácto"))
    valor = models.CharField(max_length=150)
    preferido = models.BooleanField(blank=False)
    publico = models.BooleanField(blank=False)

    class Meta:
        ordering = ['-created']
