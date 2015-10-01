# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0004_auto_20150811_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorship',
            name='end_date',
            field=models.DateField(verbose_name='Fecha de finalización', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentorship',
            name='start_date',
            field=models.DateField(verbose_name='Fecha de inicio', auto_now_add=True),
            preserve_default=True,
        ),
    ]
