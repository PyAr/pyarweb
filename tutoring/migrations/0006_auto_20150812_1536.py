# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0005_auto_20150812_1233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apprentice',
            old_name='user',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='mentor',
            old_name='user',
            new_name='owner',
        ),
    ]
