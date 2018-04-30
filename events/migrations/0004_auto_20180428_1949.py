# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_eventparticipation_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventparticipation',
            name='gender',
            field=models.CharField(verbose_name='género', default='', max_length=32, choices=[('female', 'femenino'), ('male', 'masculino'), ('Otro', 'otro')], blank=True),
        ),
    ]
