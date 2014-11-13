from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel

# Create your models here.
class Company(models.Model):
    """A PyAr Company that use Python."""

    photo = models.ImageField(upload_to='static/pycompanies/logos')
    link = models.URLField()
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @models.permalink
    def get_absolute_url(self):
        return ('company_view', (self.id,), {})

    def __unicode__(self):
        return u'%s' % self.name
