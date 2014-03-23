from django import forms
from django.utils.translation import ugettext as _
from .models import Padawan, Jedi
from taggit.forms import TagField


class PadawanForm(forms.ModelForm):
    """A PyAr Padawan form."""
    class Meta:
        model = Padawan
        fields = ('description', 'interests')

    interests = TagField(label='Interests')

    def clean(self):
        user = self.cleaned_data['user']
        if Padawan.objects.filter(user=user).exists():
            raise forms.ValidationError(_('You already are register as a Padawan'))


class JediForm(forms.ModelForm):
    """A PyAr Jedi form."""
    class Meta:
        model = Jedi
        fields = ('description', 'available', 'skills')

    skills = TagField(label='What i can teach...')
    user = forms.CharField(widget=forms.widgets.HiddenInput())
