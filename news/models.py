from django.db import models


class NewsArticle(models.Model):
    """A PyAr news article."""

    title = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.title
