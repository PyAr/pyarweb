from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    """A PyAr companies form."""
    class Meta:
        model = Company
        fields = ('name', 'photo', 'link', 'description')
