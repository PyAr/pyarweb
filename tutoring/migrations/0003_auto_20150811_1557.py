# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0002_auto_20150807_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='apprentices',
            field=models.ManyToManyField(to='tutoring.Apprentice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='looking_for',
            field=models.CharField(choices=[('M', 'Buscando mentor'), ('A', 'Buscando aprendiz')], default='M', max_length=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='mentors',
            field=models.ManyToManyField(to='tutoring.Mentor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='multiple_apprentices',
            field=models.BooleanField(default=True, verbose_name='Múltiples aprendices'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='multiple_mentors',
            field=models.BooleanField(default=True, verbose_name='Múltiples mentores'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('O', 'Abierto'), ('I', 'En curso'), ('C', 'Cerrado')], default='O', max_length=1),
            preserve_default=True,
        ),
    ]
