from django.shortcuts import render
from news.models import NewsArticle


def homepage(request):
    news = NewsArticle.objects.order_by('-created')[:3]
    return render(request, 'community/index.html', {'news': news})
