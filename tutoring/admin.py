from django.contrib import admin
from .models import Mentor, Mentorship, Apprentice


# admin.site.register([Project, Mentor, Mentorship, Apprentice])
admin.site.register([Mentor, Mentorship, Apprentice])
