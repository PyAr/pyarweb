from django.db import models
from django.contrib.auth.models import User
from taggit_autosuggest.managers import TaggableManager


class NewsArticle(models.Model):
    """A PyAr news article."""

    body = models.TextField()
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __unicode__(self):
        return u'%s' % self.title
