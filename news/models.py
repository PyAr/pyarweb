from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from taggit_autosuggest.managers import TaggableManager
from model_utils.models import TimeStampedModel


class NewsArticle(TimeStampedModel):

    """A PyAr news article."""

    title = models.CharField(max_length=255, verbose_name=_('Título'))
    introduction = models.TextField(null=True, blank=True,
                                    verbose_name=_('Introducción'))
    body = models.TextField(verbose_name=_('Contenido'))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    tags = TaggableManager(verbose_name=_('Etiquetas'), blank=True)

    @models.permalink
    def get_absolute_url(self):
        return 'news_view', (self.id,), {}

    def __unicode__(self):
        return u'{0}'.format(self.title)

    class Meta:
        ordering = ('-created',)
