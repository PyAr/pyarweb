# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Título', max_length=100)),
                ('description', models.TextField(verbose_name='Descripcion')),
                ('place', models.CharField(verbose_name='Lugar', max_length=100)),
                ('lat', models.CharField(max_length=20)),
                ('lng', models.CharField(max_length=20)),
                ('zoom', models.IntegerField(default=4)),
                ('address', models.CharField(verbose_name='Direccion', max_length=100)),
                ('url', models.URLField(null=True, blank=True)),
                ('start_at', models.DateTimeField(null=True, verbose_name='Comienza a las', blank=True)),
                ('end_at', models.DateTimeField(null=True, verbose_name='Termina a las', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
