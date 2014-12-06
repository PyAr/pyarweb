from django import forms
from django.utils.translation import ugettext as _
from .models import Padawan, Jedi
from taggit.forms import TagField


class PadawanForm(forms.ModelForm):
    """A PyAr Padawan form."""
    class Meta:
        model = Padawan
        fields = ('description', 'interests')

    interests = TagField(label=_("Intereses"))


class JediForm(forms.ModelForm):
    """A PyAr Jedi form."""
    class Meta:
        model = Jedi
        fields = ('description', 'available', 'skills')

    skills = TagField(label=_("Lo que puedo enseñar"))
