from django.contrib import admin

from .models import JobOffer, JobOfferComment


admin.site.register(JobOffer)
admin.site.register(JobOfferComment)
