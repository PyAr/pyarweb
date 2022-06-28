from django.contrib import admin
from .models import Company, UserCompanyProfile


class UserCompanyProfileAdmin(admin.ModelAdmin):
    search_fields = ('company__name', )
    autocomplete_fields = ('user', 'company')


class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name', )


admin.site.register(Company, CompanyAdmin)
admin.site.register(UserCompanyProfile, UserCompanyProfileAdmin)
