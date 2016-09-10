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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='nombre, nick, alias...', max_length=100)),
                ('email', models.EmailField(verbose_name='email', max_length=255)),
                ('interest', models.TextField(verbose_name='intereses', null=True)),
                ('seniority', models.CharField(verbose_name='experiencia', blank=True, choices=[('Trainee', 'Trainee'), ('Junior', 'Junior'), ('Semi Senior', 'Semi Senior'), ('Senior', 'Senior')], default='', max_length=100)),
                ('confirmed', models.BooleanField(verbose_name='Participación confirmada', default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(to='events.Event', related_name='participants')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
