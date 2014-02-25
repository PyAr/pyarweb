# -*- coding: utf-8 -*-

from django import forms
from .models import NewsArticle


class NewsArticleForm(forms.ModelForm):
    """A PyAr news article form."""
    class Meta:
        model = NewsArticle
        fields = ('title', 'body')
