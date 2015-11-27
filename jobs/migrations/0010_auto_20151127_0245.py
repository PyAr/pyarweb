# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_auto_20150930_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobinactivated',
            name='reason',
            field=models.CharField(max_length=100, verbose_name='Motivo', choices=[('No es un trabajo relacionado con Python', 'No es un trabajo relacionado con Python'), ('Spam', 'Spam'), ('Información insuficiente', 'Información insuficiente')]),
            preserve_default=True,
        ),
    ]
