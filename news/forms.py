# -*- coding: utf-8 -*-

from django import forms
from .models import NewsArticle
from django_summernote.widgets import SummernoteWidget


class NewsArticleForm(forms.ModelForm):
    """A PyAr news article form."""

    body = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = NewsArticle
        fields = ('title', 'body', 'tags')
