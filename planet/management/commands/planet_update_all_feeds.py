#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.management.base import NoArgsCommand

from planet.tasks import process_feed, update_feeds
from planet.models import Feed


class Command(NoArgsCommand):
    help = "Update all feeds"

    def handle(self, *args, **options):
        update_feeds.delay()

