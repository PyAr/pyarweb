# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


def view(request, new_id):
    """Show a NewsArticle."""

    newArticle = get_object_or_404(
        NewsArticle,
        id=new_id
    )

    context = dict(newArticle=newArticle)
    return render(request, 'news/view.html', context)


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
    news_tags = []

    if request.method == 'GET':
        included_tags = []
        excluded_tags = []
        for k, v in request.GET.items():
            if k.startswith('tag_'):
                if v == '1':
                    included_tags.append(k[4:])
                elif v == '2':
                    excluded_tags.append(k[4:])


        if included_tags:
            news = news.filter(tags__name__in=included_tags).distinct()
        if excluded_tags:
            news = news.exclude(tags__name__in=excluded_tags).distinct()

        news_tags = NewsArticle.tags.all()

    paginator = Paginator(news, 20) # Show 20 news per page
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    context = dict(news=news, tags=news_tags)
    return render(request, 'news/all.html', context)


