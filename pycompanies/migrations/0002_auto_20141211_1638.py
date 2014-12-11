# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycompanies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='link',
            field=models.URLField(help_text='Dirección web de la empresa', verbose_name='URL'),
            preserve_default=True,
        ),
    ]
