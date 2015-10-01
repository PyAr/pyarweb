# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apprentice',
            name='notifications_ignored',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='notifications_ignored',
        ),
        migrations.AlterField(
            model_name='apprentice',
            name='interests',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', verbose_name='Intereses', help_text='A comma-separated list of tags.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='skills',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', verbose_name='Skills', help_text='A comma-separated list of tags.'),
            preserve_default=True,
        ),
    ]
