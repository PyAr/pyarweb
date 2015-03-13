# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20150308_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, default='', editable=False),
            preserve_default=False,
        ),
    ]
