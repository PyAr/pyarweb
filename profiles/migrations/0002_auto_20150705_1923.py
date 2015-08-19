# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilesmedioscontactos',
            name='medio_contacto',
            field=models.ForeignKey(verbose_name='Medio de contácto', to='profiles.MediosContactos'),
            preserve_default=True,
        ),
    ]
