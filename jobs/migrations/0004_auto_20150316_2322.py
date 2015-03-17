# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_slug(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Job = apps.get_model("jobs", "Job")
    for j in Job.objects.all():
        j.save()


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_job_slug'),
    ]

    operations = [
            migrations.RunPython(update_slug)
    ]
