from django.db import models
from django.contrib.auth.models import User
from taggit_autosuggest.managers import TaggableManager
from model_utils.models import TimeStampedModel


class NewsArticle(TimeStampedModel):
    """A PyAr news article."""

    title = models.CharField(max_length=255)
    introduction = models.TextField(null=True, blank=True)
    body = models.TextField()
    owner = models.ForeignKey(User)
    tags = TaggableManager()

    @models.permalink
    def get_absolute_url(self):
        return ('news_view', (self.id,), {})

    def __unicode__(self):
        return u'%s' % self.title
