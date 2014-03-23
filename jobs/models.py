from django.db import models
from django.contrib.auth.models import User
from taggit_autosuggest.managers import TaggableManager
from pycompanies.models import Company

# Create your models here.
class Job(models.Model):
    """A PyAr Job."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    remote = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return "/jobs/%i/" % self.id