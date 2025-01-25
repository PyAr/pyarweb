from django import forms
from django.contrib import admin
from django_summernote.widgets import SummernoteWidget

from .models import NewsArticle


class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ('title', 'introduction', 'owner', )
        widgets = {'body': SummernoteWidget()}


@admin.register(NewsArticle)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
