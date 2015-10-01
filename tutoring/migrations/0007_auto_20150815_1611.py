# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0006_auto_20150812_1536'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apprentice',
            old_name='interests',
            new_name='tags',
        ),
        migrations.RenameField(
            model_name='mentor',
            old_name='skills',
            new_name='tags',
        ),
    ]
