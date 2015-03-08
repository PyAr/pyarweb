# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20141211_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='event',
            name='lng',
        ),
        migrations.RemoveField(
            model_name='event',
            name='zoom',
        ),
    ]
