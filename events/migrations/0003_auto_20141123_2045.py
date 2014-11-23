# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20141123_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='zoom',
            field=models.IntegerField(default=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='end_at',
            field=models.DateTimeField(verbose_name='Termina a las', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_at',
            field=models.DateTimeField(verbose_name='Comienza a las', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.URLField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
