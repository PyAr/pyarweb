# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0011_auto_20150816_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apprentice',
            name='status',
            field=models.CharField(verbose_name='Estado', max_length=1, choices=[('T', 'Entretenando'), ('I', 'Inactivo'), ('W', 'Buscando mentor')], default='W'),
            preserve_default=True,
        ),
    ]
