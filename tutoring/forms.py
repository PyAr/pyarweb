from django import forms
from .models import Mentor, Apprentice, Project
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Submit, Reset, Layout
from crispy_forms.helper import FormHelper


class MentorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MentorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('mentor_submit', _('Guardar')))
        self.helper.add_input(Reset('mentor_reset', _('Limpiar'),
                                    css_class='btn-default'))
    class Meta:
        model = Mentor
        exclude = ('user',)


class ApprenticeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ApprenticeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('apprentice_submit', _('Guardar')))
        self.helper.add_input(Reset('apprentice_reset', _('Limpiar'),
                                    css_class='btn-default'))
    class Meta:
        model = Apprentice
        exclude = ('user',)


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('apprentice_submit', _('Guardar')))
        self.helper.add_input(Reset('apprentice_reset', _('Limpiar'),
                                    css_class='btn-default'))
    class Meta:
        model = Project
        exclude = ('owner',)