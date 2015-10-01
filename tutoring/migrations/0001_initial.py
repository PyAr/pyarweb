# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apprentice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.TextField(verbose_name='Descripción', null=True, blank=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('notifications_ignored', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(default='W', choices=[('T', 'Entretenando'), ('I', 'Inactivo'), ('W', 'Buscando mentor')], max_length=1)),
                ('interests', taggit.managers.TaggableManager(through='taggit.TaggedItem', verbose_name='Tags', to='taggit.Tag', help_text='A comma-separated list of tags.')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('available', models.BooleanField(verbose_name='Disponible', default=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('notifications_ignored', models.PositiveIntegerField(default=0)),
                ('slots', models.PositiveIntegerField(default=2, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(1)])),
                ('skills', taggit.managers.TaggableManager(through='taggit.TaggedItem', verbose_name='Tags', to='taggit.Tag', help_text='A comma-separated list of tags.')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mentorship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de inicio')),
                ('end_date', models.DateTimeField(verbose_name='Fecha de finalización', null=True, blank=True)),
                ('blog_link', models.URLField(verbose_name='URL del blog', blank=True)),
                ('apprentice', models.ForeignKey(verbose_name='Aprendiz', to='tutoring.Apprentice')),
                ('mentor', models.ForeignKey(verbose_name='Mentor', to='tutoring.Mentor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.TextField(verbose_name='Descripción', blank=True)),
                ('title', models.CharField(verbose_name='Título', max_length=250)),
                ('link_repo', models.URLField(verbose_name='URL del repositorio', blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(through='taggit.TaggedItem', verbose_name='Tags', to='taggit.Tag', help_text='A comma-separated list of tags.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mentorship',
            name='project',
            field=models.ForeignKey(verbose_name='Proyecto', to='tutoring.Project'),
            preserve_default=True,
        ),
    ]
