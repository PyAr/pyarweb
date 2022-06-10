from django.contrib import admin
from .models import Company, UserCompanyProfile


class UserCompanyProfileAdmin(admin.ModelAdmin):
    search_fields = ('company__name', )


admin.site.register(Company)
admin.site.register(UserCompanyProfile, UserCompanyProfileAdmin)
