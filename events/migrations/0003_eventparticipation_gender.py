# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20170325_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventparticipation',
            name='gender',
            field=models.CharField(verbose_name='género', blank=True, choices=[('female', 'female'), ('male', 'fale'), ('Otro', 'other')], max_length=32, default=''),
        ),
    ]
