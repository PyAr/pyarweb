# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
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


@login_required
def delete(request, new_id):
    """Delete a NewsArticle."""

    newArticle = get_object_or_404(
        NewsArticle,
        id=new_id,
        owner=request.user,
    )
    newArticle.delete()
    url = reverse('news_list_all')

    return HttpResponseRedirect(url)


@login_required
def update(request, new_id):
    """Update a NewsArticle."""

    newArticle = get_object_or_404(
        NewsArticle,
        id=new_id,
        owner=request.user,
    )

    if request.method == 'POST':
        form = NewsArticleForm(request.POST)
        if form.is_valid():
            newArticle.title = form.instance.title
            newArticle.body = form.instance.body
            newArticle.save()
            url = reverse('news_list_all')
            return HttpResponseRedirect(url)
    else:
        form = NewsArticleForm(
            dict(
                title=newArticle.title,
                body=newArticle.body
            )
        )

    context = dict(
        form=form,
        newArticle=newArticle
    )
    return render(request, 'news/update.html', context)


def list_all(request):
    """Return all news articles ordered by date desc."""
    news = NewsArticle.objects.order_by('-created')
    context = dict(news=news)
    return render(request, 'news/all.html', context)
