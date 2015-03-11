from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.conf.urls import patterns, url
from .models import NewsArticle
from .views import (
    NewsArticleCreate,
    NewsArticleDelete,
    NewsArticleList,
    NewsArticleUpdate,
    NewsArticleListTag,
    NewsFeed
)


urlpatterns = patterns('',
                       url(r'^$', NewsArticleList.as_view(),
                           name='news_list_all'),
                       url(r'^rss$', NewsFeed(),
                           name='news_feed'),
                       url(r'^add/$',
                           login_required(NewsArticleCreate.as_view()),
                           name='news_add'),
                       url(r'^(?P<pk>\d+)/$',
                           DetailView.as_view(model=NewsArticle),
                           name='news_view'),
                       url(r'^(?P<pk>\d+)/delete/$',
                           login_required(NewsArticleDelete.as_view()),
                           name='news_delete'),
                       url(r'^(?P<pk>\d+)/update/$',
                           login_required(NewsArticleUpdate.as_view()),
                           name='news_update'),
                       url(r'^tag/(?P<tag>[\w-]+)/$',
                           login_required(NewsArticleListTag.as_view()),
                           name='news_tags_list'),
                       )
