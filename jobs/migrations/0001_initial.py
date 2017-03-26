# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.utils.timezone
import model_utils.fields
import taggit_autosuggest.managers
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
        ('pycompanies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('location', models.CharField(max_length=100, verbose_name='Lugar')),
                ('email', models.EmailField(max_length=254)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('remote_work', models.BooleanField(default=False, verbose_name='Trabajo Remoto')),
                ('seniority', models.CharField(max_length=100, default='', blank=True, verbose_name='Experiencia', choices=[('Trainee', 'Trainee'), ('Junior', 'Junior'), ('Semi Senior', 'Semi Senior'), ('Senior', 'Senior')])),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(null=True, to='pycompanies.Company', blank=True, verbose_name='Empresa')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tags', taggit_autosuggest.managers.TaggableManager(through='taggit.TaggedItem', to='taggit.Tag', help_text='A comma-separated list of tags.', verbose_name='Etiquetas')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='JobInactivated',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('reason', models.CharField(max_length=100, verbose_name='Motivo', choices=[('No es un trabajo relacionado con Python', 'No es un trabajo relacionado con Python'), ('Spam', 'Spam'), ('Información insuficiente', 'Información insuficiente')])),
                ('comment', models.TextField(null=True, blank=True, verbose_name='Comentario')),
                ('job', models.ForeignKey(to='jobs.Job')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
