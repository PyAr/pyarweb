# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0003_auto_20150811_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='apprentices',
            field=models.ManyToManyField(to='tutoring.Apprentice', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='mentors',
            field=models.ManyToManyField(to='tutoring.Mentor', blank=True),
            preserve_default=True,
        ),
    ]
