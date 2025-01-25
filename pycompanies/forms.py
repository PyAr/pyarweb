from django import forms
from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, ButtonHolder, Layout, Submit

from .models import Company, UserCompanyProfile

class CompanyForm(forms.ModelForm):
    """A PyAr companies form."""

    description = forms.CharField(widget=SummernoteInplaceWidget())
    link = forms.CharField(
        help_text=_('Por favor, ingrese una URL válida con esquema (por ejemplo, https://).')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                'name',
                'photo',
                'link',
                'description'
            ),
            ButtonHolder(
                Submit(_('Guardar'), _('Guardar'), css_class='btn btn-default')
            )
        )

    def clean_link(self):
        link = self.cleaned_data.get('link')
        if link and not urlparse(link).scheme:
            link = f'https://{link}'
        return link

    class Meta:
        fields = ['name', 'photo', 'link', 'description']
        model = Company

class UserCompanyForm(forms.ModelForm):
    """A PyAr user companies form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                'user'
            ),
            ButtonHolder(
                Submit(_('Guardar'), _('Guardar'), css_class='btn btn-default')
            )
        )

    class Meta:
        fields = ['user']
        model = UserCompanyProfile
