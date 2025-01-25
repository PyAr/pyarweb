from django.contrib import admin

from .models import Company, UserCompanyProfile


@admin.register(UserCompanyProfile)
class UserCompanyProfileAdmin(admin.ModelAdmin):
    search_fields = ('company__name', )
    autocomplete_fields = ('user', 'company')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name', )
