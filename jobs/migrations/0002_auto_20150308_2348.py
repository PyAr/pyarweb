# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='remote_work',
            field=models.BooleanField(default=False, verbose_name='Trabajo Remoto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='seniority',
            field=models.CharField(default='', max_length=100, verbose_name='Experiencia', blank=True, choices=[('Trainee', 'Trainee'), ('Junior', 'Junior'), ('Semi Senior', 'Semi Senior'), ('Senior', 'Senior')]),
            preserve_default=True,
        ),
    ]
