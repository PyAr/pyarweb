# -*- coding: utf-8 -*-

from django import forms
from .models import Project
from taggit.forms import TagWidget


class ProjectForm(forms.ModelForm):
    """A PyAr news article form."""
    class Meta:
        model = Project
        fields = ('name', 'description', 'repositoryType', 'repository', 'license', 'state', 'tags', 'mail', 'contribution', 'logo')
        labels = {
            'name': 'Nombre',
            'mail': 'Email',
            'description': 'Descripción',
            'repositoryType': 'Host del Repositorio',
            'repository': 'URL del repositorio',
            'license': 'Licencia del software',
            'state': 'Estado del proyecto',
            'contribution': 'Abierto a Contribuciones'
        }
        help_texts = {
            'name': 'Nombre del proyecto',
            'mail': 'Lista de correo o email para ponerse en contacto',
            'description': 'Descripción del proyecto',
            'repositoryType': 'Donde está hosteado el sistema de versionado del proyecto',
            'repository': 'URL del repositorio del proyecto',
            'license': 'Bajo que licenciacia se distribuye el proyecto',
            'state': 'Si el proyecto se encuentra activo o inactivo',
            'contribution': 'Abierto a contribuciones de la comunidad',
        }
        widgets = {
            'tags': TagWidget(),
        }

