from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.urls import path

from .models import NewsArticle
from .views import (
    NewsArticleCreate,
    NewsArticleDelete,
    NewsArticleList,
    NewsArticleUpdate,
    NewsFeed
)

urlpatterns = [
    path('', NewsArticleList.as_view(), name='news_list_all'),
    path('rss', NewsFeed(), name='news_feed'),
    path('add/', login_required(NewsArticleCreate.as_view()), name='news_add'),
    path('<int:pk>/', DetailView.as_view(model=NewsArticle), name='news_view'),
    path('<int:pk>/delete/', login_required(NewsArticleDelete.as_view()), name='news_delete'),
    path('<int:pk>/update/', login_required(NewsArticleUpdate.as_view()), name='news_update'),
]
