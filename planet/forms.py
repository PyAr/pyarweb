from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.conf import settings

import feedparser

from crispy_forms.layout import Submit, Reset
from crispy_forms.helper import FormHelper

from planet.models import Feed

SEARCH_CHOICES = (
    ("posts", _("Posts")),
    ("tags", _("Tags")),
    ("blogs", _("Blogs")),
    ("authors", _("Authors")),
    ("feeds", _("Feeds")),
)


class SearchForm(forms.Form):
    w = forms.ChoiceField(choices=SEARCH_CHOICES, label="")
    q = forms.CharField(max_length=100, label="")


class FeedForm(forms.Form):
    url = forms.URLField()

    def __init__(self, *args, **kwargs):
        super(FeedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('Submit', _('Guardar')))
        self.helper.add_input(
            Reset('Reset', _('Limpiar'), css_class='btn-default'))

    def clean_url(self):
        url = self.cleaned_data['url']
        if Feed.objects.filter(url=url).count() > 0:
            raise ValidationError(_('Ya existe un feed con esa URL.'))
        document = feedparser.parse(url, agent=settings.PLANET["USER_AGENT"])
        if not document.feed.get('link'):
            raise ValidationError(_('La URL ingresada no pertenece a un feed.'))
        return url
