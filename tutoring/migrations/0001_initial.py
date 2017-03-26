# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import taggit.managers
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apprentice',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('description', models.TextField(null=True, verbose_name='Descripción', blank=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('T', 'Entretenando'), ('I', 'Inactivo'), ('W', 'Buscando mentor')], default='W', max_length=1, verbose_name='Estado')),
                ('owner', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', verbose_name='Intereses', to='taggit.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('available', models.BooleanField(verbose_name='Disponible', default=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('slots', models.PositiveIntegerField(default=2, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(1)])),
                ('owner', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', verbose_name='Skills', to='taggit.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Mentorship',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='Fecha de inicio')),
                ('end_date', models.DateField(null=True, verbose_name='Fecha de finalización', blank=True)),
                ('blog_link', models.URLField(null=True, verbose_name='URL del blog', blank=True)),
                ('status', models.CharField(choices=[('I', 'En curso'), ('O', 'En espera'), ('C', 'Cerrado')], default='I', max_length=1, verbose_name='Estado')),
                ('apprentice', models.ForeignKey(to='tutoring.Apprentice', verbose_name='Aprendiz')),
                ('owner', models.ForeignKey(to='tutoring.Mentor', verbose_name='Mentor')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='Título', max_length=250)),
                ('description', models.TextField(verbose_name='Descripción', blank=True)),
                ('status', models.CharField(choices=[('O', 'Abierto'), ('I', 'En curso'), ('C', 'Cerrado')], default='O', max_length=1)),
                ('link_repo', models.URLField(verbose_name='URL del repositorio', blank=True)),
                ('looking_for', models.CharField(choices=[('M', 'Buscando mentor'), ('A', 'Buscando aprendiz')], default='M', max_length=1)),
                ('multiple_mentors', models.BooleanField(verbose_name='Múltiples mentores', default=True)),
                ('multiple_apprentices', models.BooleanField(verbose_name='Múltiples aprendices', default=True)),
                ('apprentices', models.ManyToManyField(to='tutoring.Apprentice', blank=True)),
                ('mentors', models.ManyToManyField(to='tutoring.Mentor', blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', verbose_name='Tags', to='taggit.Tag')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='mentorship',
            name='project',
            field=models.ForeignKey(to='tutoring.Project', null=True, verbose_name='Proyecto', blank=True),
        ),
    ]
