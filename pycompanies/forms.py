from django import forms
from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, ButtonHolder, Layout, Submit

from .models import Company, UserCompanyProfile


class CompanyForm(forms.ModelForm):
    """A PyAr companies form."""

    description = forms.CharField(widget=SummernoteInplaceWidget())

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
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
