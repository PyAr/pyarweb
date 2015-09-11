# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0009_mentorship_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorship',
            name='status',
            field=models.CharField(max_length=1, verbose_name='Estado', default='I', choices=[('O', 'En espera'), ('I', 'En curso'), ('C', 'Cerrado')]),
            preserve_default=True,
        ),
    ]
