from django import forms
from .models import Mentor, Apprentice, Project, Mentorship
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Submit, Reset, Layout
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


# class ProjectForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super(ProjectForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.add_input(Submit('project_submit', _('Guardar')))
#         self.helper.add_input(Reset('project_reset', _('Limpiar'),
#                                     css_class='btn-default'))
#
#     class Meta:
#         model = Project
#         exclude = ('owner',)


class MentorshipForm(forms.ModelForm):

    def __init__(self, mentor, *args, **kwargs):
        super(MentorshipForm, self).__init__(*args, **kwargs)
        self.mentor = mentor
        self.helper = FormHelper()
        self.helper.add_input(Submit('mentorship_submit', _('Guardar')))
        self.helper.add_input(Reset('mentorship_reset', _('Limpiar'),
                                    css_class='btn-default'))

    def clean(self):
        max_slots = self.mentor.slots
        mentorships = self.mentor.mentorship_set.filter(status=Mentorship.STATUS_IN_COURSE).count()
        if mentorships >= max_slots:
            raise ValidationError(u'No te quedan slots disponibles')

    class Meta:
        model = Mentorship
        exclude = ('owner', 'project',)
