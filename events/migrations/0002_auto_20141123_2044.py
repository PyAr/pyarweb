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
            name='zoom',
        ),
        migrations.AlterField(
            model_name='event',
            name='end_at',
            field=models.DateTimeField(default=None, verbose_name='Termina a las'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_at',
            field=models.DateTimeField(default=None, verbose_name='Comienza a las'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
