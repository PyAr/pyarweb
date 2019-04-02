# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20180429_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, blank=True, null=True, populate_from='name', editable=True),
        ),
    ]
