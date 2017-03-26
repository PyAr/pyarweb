from django import forms
from .models import Mentor, Apprentice, Project, Mentorship
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Submit, Reset
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError


class MentorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MentorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('mentor_submit', _('Guardar')))
        self.helper.add_input(Reset('mentor_reset', _('Limpiar'),
                                    css_class='btn-default'))

    class Meta:
        model = Mentor
        exclude = ('owner',)


class ApprenticeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ApprenticeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('apprentice_submit', _('Guardar')))
        self.helper.add_input(Reset('apprentice_reset', _('Limpiar'),
                                    css_class='btn-default'))

    class Meta:
        model = Apprentice
        exclude = ('owner',)


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('project_submit', _('Guardar')))
        self.helper.add_input(Reset('project_reset', _('Limpiar'),
                                    css_class='btn-default'))

    class Meta:
        model = Project
        exclude = ('owner',)


class MentorshipForm(forms.ModelForm):

    def __init__(self, mentor=None, *args, **kwargs):
        super(MentorshipForm, self).__init__(*args, **kwargs)
        if mentor is not None:
            self.instance.owner = mentor
        self.helper = FormHelper()
        self.helper.add_input(Submit('mentorship_submit', _('Guardar')))
        self.helper.add_input(Reset('mentorship_reset', _('Limpiar'),
                                    css_class='btn-default'))

    def clean(self):
        active = Mentorship.STATUS_IN_COURSE
        status = self.cleaned_data.get('status')
        if status == active:
            mentor = self.instance.owner
            max_slots = mentor.slots
            mentorships = mentor.mentorship_set.filter(status=active)
            if self.instance.pk:
                mentorships = mentorships.exclude(id=self.instance.pk)
            mentorships = mentorships.count()
            if mentorships >= max_slots:
                raise ValidationError(u'No te quedan slots disponibles.')

    class Meta:
        model = Mentorship
        exclude = ('owner', 'project',)
