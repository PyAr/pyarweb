from django.contrib import admin
from django.db import models
from .models import Job, JobInactivated


admin.site.register(Job)
admin.site.register(JobInactivated)
