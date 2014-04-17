# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    """A PyAr events."""

    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.TextField()
    place = models.CharField(max_length=100)
    lat = models.CharField(max_length=20)
    lng = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    url = models.URLField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s by %s" % (self.name, self.owner)
