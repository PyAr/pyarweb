from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    """A PyAr Jobs form."""
    class Meta:
        model = Job
        fields = ('title', 'description', 'link', 'tags')
