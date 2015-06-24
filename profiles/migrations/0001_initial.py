# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import taggit_autosuggest.managers
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MediosContactos',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('nombre', models.CharField(max_length=150)),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('tutor', models.BooleanField(default=False, verbose_name='Querés enseñar?')),
                ('tutorado', models.BooleanField(default=False, verbose_name='Querés recibir ayuda de un tutor?')),
                ('disponibilidad_semanal', models.IntegerField(verbose_name='Cantidad de horas semanales')),
                ('intereses', taggit_autosuggest.managers.TaggableManager(help_text='A comma-separated list of tags.', blank=True, verbose_name='Que temas te interesan?', to='taggit.Tag', through='taggit.TaggedItem')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProfilesMediosContactos',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('valor', models.CharField(max_length=150)),
                ('preferido', models.BooleanField()),
                ('publico', models.BooleanField()),
                ('medio_contacto', models.ForeignKey(to='profiles.MediosContactos')),
                ('profile', models.ForeignKey(to='profiles.Profiles')),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
    ]
