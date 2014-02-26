from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    """A PyAr companies form."""
    class Meta:
        model = Company
        fields = ('photo', 'link', 'description')
