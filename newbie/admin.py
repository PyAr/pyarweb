from django.contrib import admin
from .models import (
    Project,
    Jedi,
    Padawan,
)

admin.site.register(Project)
admin.site.register(Jedi)
admin.site.register(Padawan)
