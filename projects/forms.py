# -*- coding: utf-8 -*-

from django import forms
from .models import Project
from taggit.forms import TagWidget


class ProjectForm(forms.ModelForm):
    """A PyAr news article form."""
    class Meta:
        model = Project
        fields = ('name', 'description', 'repositoryType', 'repository', 'license', 'state', 'tags', 'mail', 'contribution', 'logo')
        #widgets = {
        #    'tags': TagWidget(),
        #}

