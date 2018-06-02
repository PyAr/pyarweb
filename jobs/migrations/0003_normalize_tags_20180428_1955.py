# -*- coding: utf-8 -*-
from django.db import migrations, models
from taggit.models import TaggedItem, Tag  # can be used since Models are actually not modified
from django.contrib.contenttypes.models import ContentType

from jobs.utils import normalize


def clean_tags(apps, schema_editor):
    """Normalize all tags, fix tagged-objects and remove (now unused) not-normalized tags."""

    all_tags = Tag.objects.all()
    n_tags = all_tags.count()
    for bad_tag in all_tags:
        normalized = normalize(bad_tag.name)
        if normalized == bad_tag.name:
            # Actually a good tabg
            continue
        normalized_tag, _ = Tag.objects.get_or_create(name=normalized)
        tagged_objects = TaggedItem.objects.filter(tag__id=bad_tag.id)
        for o in tagged_objects:
            # o.tags.add(normalized)
            TaggedItem.objects.create(
                tag=normalized_tag,
                content_type=ContentType.objects.get_for_model(o),
                object_id=o.id
            )
        Tag.objects.filter(id=bad_tag.id).delete()

    annotated = Tag.objects.annotate(count=models.Count('taggit_taggeditem_items'))
    annotated.filter(count=0).delete()
    print(" Deleted {} tags".format(n_tags - Tag.objects.count()), end='')


class Migration(migrations.Migration):
    dependencies = [
        ('jobs', '0002_auto_20170326_1616'),
        ('taggit', '0002_auto_20150616_2121')
    ]

    operations = [
        migrations.RunPython(clean_tags, reverse_code=migrations.RunPython.noop),
    ]
