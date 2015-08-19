# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0004_auto_20150705_1923'),
        ('profiles', '0002_auto_20150705_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='ciudad',
            field=models.ForeignKey(default=1, to='cities_light.City'),
            preserve_default=False,
        ),
    ]
