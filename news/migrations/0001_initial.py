# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit_autosuggest.managers
import django.utils.timezone
import model_utils.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=255, verbose_name='Título')),
                ('introduction', models.TextField(null=True, verbose_name='Introducción', blank=True)),
                ('body', models.TextField(verbose_name='Contenido')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tags', taggit_autosuggest.managers.TaggableManager(through='taggit.TaggedItem', help_text='A comma-separated list of tags.', blank=True, to='taggit.Tag', verbose_name='Etiquetas')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
