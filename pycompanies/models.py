from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Company(TimeStampedModel):
    """A PyAr Company that use Python."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='companies')
    name = models.CharField('Nombre', max_length=255, unique=True)
    description = models.TextField('Descripción')
    photo = models.ImageField('Logo', upload_to='pycompanies/logos')
    link = models.URLField('URL',
                           help_text=_('Dirección web de la empresa')
                           )

    def get_absolute_url(self):
        return reverse('companies:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return u'%s' % self.name


#  SIGNALS

@receiver(post_delete, sender=Company)
def post_delete_user(sender, instance, *args, **kwargs):
    "Delete logo image after delete company"

    instance.photo.delete(save=False)
