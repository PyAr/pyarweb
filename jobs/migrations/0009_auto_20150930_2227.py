# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_auto_20150926_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobInactivated',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('reason', models.CharField(verbose_name='Motivo/Razón', max_length=100, choices=[('No es un aviso relacionado con Python', 'No es un aviso relacionado con Python'), ('Spam', 'Spam')])),
                ('comment', models.TextField(verbose_name='Comentario', blank=True, null=True)),
                ('job', models.ForeignKey(to='jobs.Job')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-created']},
        ),
    ]
