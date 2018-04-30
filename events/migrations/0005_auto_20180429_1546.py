# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20180428_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='name', editable=True, unique=True, blank=True, null=True, verbose_name='Url'),
        ),
    ]
