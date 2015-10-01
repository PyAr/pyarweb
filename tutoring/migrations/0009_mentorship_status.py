# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0008_auto_20150816_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentorship',
            name='status',
            field=models.CharField(choices=[('O', 'Abierto'), ('I', 'En curso'), ('C', 'Cerrado')], default='O', verbose_name='Estado', max_length=1),
            preserve_default=True,
        ),
    ]
