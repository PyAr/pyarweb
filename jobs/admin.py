from django.contrib import admin
from django.db import models
from .models import Job


class Jobs(Job):
    """
    All Jobs, actives and inactives
    """
    class Meta:
        proxy = True
        verbose_name = "Job"

    objects = models.Manager()

admin.site.register(Jobs)
