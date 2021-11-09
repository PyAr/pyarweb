# Generated by Django 3.2.9 on 2021-11-09 16:02

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20180429_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=True, null=True, populate_from='name', unique=True),
        ),
    ]
