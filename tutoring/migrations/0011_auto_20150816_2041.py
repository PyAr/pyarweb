# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0010_auto_20150816_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorship',
            name='status',
            field=models.CharField(choices=[('I', 'En curso'), ('O', 'En espera'), ('C', 'Cerrado')], verbose_name='Estado', max_length=1, default='I'),
            preserve_default=True,
        ),
    ]
