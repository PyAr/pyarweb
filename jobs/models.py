from django.db import models
from django.contrib.auth.models import User
from taggit_autosuggest.managers import TaggableManager

# Create your models here.
class Job(models.Model):
    """A PyAr Job."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    owner = models.ForeignKey(User, related_name='company_user')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __unicode__(self):
        return u'%s' % self.title
