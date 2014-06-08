from django import forms
from django.contrib import admin
from .models import NewsArticle
from django_summernote.widgets import SummernoteWidget


class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        widgets = {'body': SummernoteWidget()}


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm

admin.site.register(NewsArticle, NewsAdmin)
