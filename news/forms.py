# -*- coding: utf-8 -*-

from django import forms


class NewsArticleForm(forms.Form):
    """A PyAr news article form."""

    title =  forms.CharField(max_length=255)
    body = forms.Textarea()

