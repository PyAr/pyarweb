# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pycompanies', '0002_auto_20141211_1638'),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('location', models.CharField(max_length=100, verbose_name='Lugar')),
                ('email', models.EmailField(max_length=75)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('remote_work', models.BooleanField(default=False, verbose_name='Trabajo Remoto')),
                ('seniority', models.CharField(max_length=100, choices=[('Trainee', 'Trainee'), ('Junior', 'Junior'), ('Semi Senior', 'Semi Senior'), ('Senior', 'Senior')], blank=True, verbose_name='Experiencia')),
                ('company', models.ForeignKey(null=True, blank=True, to='pycompanies.Company', verbose_name='Empresa')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tags', taggit_autosuggest.managers.TaggableManager(through='taggit.TaggedItem', to='taggit.Tag', help_text='A comma-separated list of tags.', verbose_name='Etiquetas')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
