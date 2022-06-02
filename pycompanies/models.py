from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Company(TimeStampedModel):
    """A PyAr Company that use Python."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='companies',
                              on_delete=models.CASCADE)
    name = models.CharField('Nombre', max_length=255, unique=True)
    description = models.TextField('Descripción')
    photo = models.ImageField('Logo', upload_to='pycompanies/logos')
    link = models.URLField('URL',
                           help_text=_('Dirección web de la empresa')
                           )
    rank = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('companies:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return u'%s' % self.name


class UserCompanyProfileManager(models.Manager):
    """User company profile manager."""

    def for_user(self, user, **kwargs):
        """
        Get the company object for a given user.
        """
        if user.is_anonymous:
            return None

        qs = super().get_queryset()
        return qs.filter(user=user, **kwargs).first()


class UserCompanyProfile(models.Model):
    """Company data for a User."""
    objects = UserCompanyProfileManager()

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='company',
                                on_delete=models.CASCADE)
    company = models.ForeignKey(Company,
                                related_name='users',
                                on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}: {self.company.name}'


#  SIGNALS

@receiver(post_delete, sender=Company)
def post_delete_user(sender, instance, *args, **kwargs):
    "Delete logo image after delete company"

    instance.photo.delete(save=False)
