# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import NewsArticle
from .forms import NewsArticleForm


def add(request):
    """Add a new NewsArticle."""


def latest(request):
    """Return latest news articles."""
    news = NewsArticle.objects.order_by('-created')[:5]
    context = dict(news=news)
    return render(request, 'latest.html', context)
