# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0005_auto_20150609_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='nombre, nick, alias...', max_length=100)),
                ('email', models.EmailField(verbose_name='email', max_length=255)),
                ('interest', models.TextField(verbose_name='intereses', blank=True)),
                ('seniority', models.CharField(verbose_name='experiencia', choices=[('Trainee', 'Trainee'), ('Junior', 'Junior'), ('Semi Senior', 'Semi Senior'), ('Senior', 'Senior'), ('guido', 'Soy Guido Van Rossum')], max_length=100, default='', blank=True)),
                ('cv', models.URLField(verbose_name='curriculum vitae', max_length=1024, default='', blank=True)),
                ('share_with_sponsors', models.BooleanField(verbose_name='¿Querés compartir tus datos con los sponsors?', default=False)),
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
        migrations.AddField(
            model_name='event',
            name='has_sponsors',
            field=models.BooleanField(verbose_name='¿El evento tiene sponsors?', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='registration_enabled',
            field=models.BooleanField(verbose_name='¿Habilitar inscripción', default=False),
            preserve_default=True,
        ),
    ]
