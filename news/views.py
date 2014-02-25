# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import NewsArticle
from .forms import NewsArticleForm


@login_required
def add(request):
    """Add a new NewsArticle."""

    if request.method == 'POST':
        form = NewsArticleForm(request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            url = reverse('news_list_all')
            return HttpResponseRedirect(url)
    else:
        form = NewsArticleForm()

    context = dict(form=form)
    return render(request, 'news/add.html', context)


def list_all(request):
    """Return all news articles ordered by date desc."""
    news = NewsArticle.objects.order_by('-created')
    context = dict(news=news)
    return render(request, 'news/all.html', context)
