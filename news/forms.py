from django import forms
from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset
from .models import NewsArticle


class NewsArticleForm(forms.ModelForm):
    """A PyAr news article form."""

    body = forms.CharField(widget=SummernoteInplaceWidget())

    def __init__(self, *args, **kwargs):
        super(NewsArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('job_submit', _('Guardar')))
        self.helper.add_input(Reset('job_reset', _('Limpiar'), css_class='btn-default'))

    class Meta:
        model = NewsArticle
        exclude = ('owner',)