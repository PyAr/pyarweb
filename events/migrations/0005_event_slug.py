# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150310_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, default='', unique=True),
            preserve_default=False,
        ),
    ]
