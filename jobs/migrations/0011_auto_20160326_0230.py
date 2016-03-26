# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_auto_20151127_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
