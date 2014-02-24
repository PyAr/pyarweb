from django.db import models
from django.contrib.auth.models import User


class NewsArticle(models.Model):
    """A PyAr news article."""

    body = models.TextField()
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.title
