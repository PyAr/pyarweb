# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='event',
            name='lng',
        ),
        migrations.RemoveField(
            model_name='event',
            name='zoom',
        ),
        migrations.AlterField(
            model_name='event',
            name='end_at',
            field=models.DateField(verbose_name='Termina a las', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_at',
            field=models.DateField(verbose_name='Comienza a las', blank=True, null=True),
            preserve_default=True,
        ),
    ]
