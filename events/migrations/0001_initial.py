# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descripcion')),
                ('place', models.CharField(max_length=100, verbose_name='Lugar')),
                ('address', models.CharField(max_length=100, verbose_name='Direccion')),
                ('url', models.URLField(null=True, blank=True)),
                ('start_at', models.DateTimeField(verbose_name='Comienza a las')),
                ('end_at', models.DateTimeField(verbose_name='Termina a las')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
