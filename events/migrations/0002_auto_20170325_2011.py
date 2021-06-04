# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='nombre, nick, alias...')),
                ('email', models.EmailField(max_length=255, verbose_name='email')),
                ('interest', models.TextField(verbose_name='intereses', blank=True)),
                ('seniority', models.CharField(max_length=100, verbose_name='experiencia', choices=[('Trainee', 'Trainee'), ('Junior', 'Junior'), ('Semi Senior', 'Semi Senior'), ('Senior', 'Senior'), ('guido', 'Soy Guido Van Rossum')], blank=True, default='')),
                ('cv', models.URLField(max_length=1024, verbose_name='curriculum vitae', blank=True, default='')),
                ('share_with_sponsors', models.BooleanField(verbose_name='¿Querés compartir tus datos con los sponsors?', default=False)),
                ('confirmed', models.BooleanField(verbose_name='Participación confirmada', default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='has_sponsors',
            field=models.BooleanField(verbose_name='¿El evento tiene sponsors?', default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='registration_enabled',
            field=models.BooleanField(verbose_name='¿Habilitar inscripción', default=False),
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='event',
            field=models.ForeignKey(to='events.Event', related_name='participants', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='eventparticipation',
            unique_together=set([('event', 'email')]),
        ),
    ]
