# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150609_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='registration_enabled',
            field=models.BooleanField(default=False, verbose_name='Habilitar suscripción'),
            preserve_default=True,
        ),
    ]
