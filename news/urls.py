from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.urls import re_path

from .models import NewsArticle
from .views import (
    NewsArticleCreate,
    NewsArticleDelete,
    NewsArticleList,
    NewsArticleUpdate,
    NewsFeed
)

urlpatterns = [
    re_path(r'^$', NewsArticleList.as_view(),
            name='news_list_all'),
    re_path(r'^rss$', NewsFeed(),
            name='news_feed'),
    re_path(r'^add/$',
            login_required(NewsArticleCreate.as_view()),
            name='news_add'),
    re_path(r'^(?P<pk>\d+)/$',
            DetailView.as_view(model=NewsArticle),
            name='news_view'),
    re_path(r'^(?P<pk>\d+)/delete/$',
            login_required(NewsArticleDelete.as_view()),
            name='news_delete'),
    re_path(r'^(?P<pk>\d+)/update/$',
            login_required(NewsArticleUpdate.as_view()),
            name='news_update'),
]
