# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20150705_1923'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-modified']},
        ),
        migrations.AddField(
            model_name='job',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
