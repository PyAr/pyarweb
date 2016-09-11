# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0006_event_registration_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='nombre, nick, alias...', max_length=100)),
                ('email', models.EmailField(verbose_name='email', max_length=255)),
                ('interest', models.TextField(verbose_name='intereses', blank=True)),
                ('seniority', models.CharField(verbose_name='experiencia', max_length=100, default='', blank=True, choices=[('Trainee', 'Trainee'), ('Junior', 'Junior'), ('Semi Senior', 'Semi Senior'), ('Senior', 'Senior')])),
                ('confirmed', models.BooleanField(verbose_name='Participación confirmada', default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(to='events.Event', related_name='participants')),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='eventparticipation',
            unique_together=set([('event', 'email')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_enabled',
            field=models.BooleanField(verbose_name='Habilitar inscripción', default=False),
            preserve_default=True,
        ),
    ]
