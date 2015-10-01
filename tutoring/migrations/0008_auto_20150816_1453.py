# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0007_auto_20150815_1611'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-id']},
        ),
        migrations.RenameField(
            model_name='mentorship',
            old_name='mentor',
            new_name='owner',
        ),
        migrations.AlterField(
            model_name='mentorship',
            name='blog_link',
            field=models.URLField(null=True, blank=True, verbose_name='URL del blog'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentorship',
            name='project',
            field=models.ForeignKey(null=True, to='tutoring.Project', verbose_name='Proyecto', blank=True),
            preserve_default=True,
        ),
    ]
