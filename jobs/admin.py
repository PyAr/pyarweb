from django.contrib import admin
from .models import Job, JobInactivated

admin.site.register(Job)
admin.site.register(JobInactivated)
