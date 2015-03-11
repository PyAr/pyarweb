from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView
from django.utils.translation import ugettext as _
from community.views import OwnedObject, FilterableList
from .models import NewsArticle
from .forms import NewsArticleForm
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse



class NewsFeed(Feed):
    title = "Feed de Noticias de Pyar"
    link = reverse_lazy("news_list_all")
    description = "Novedades e información de Python Argentina"

    def items(self):
        return NewsArticle.objects.order_by('-created')[0:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_pubdate(self, item):
        return item.created

    def categories(self, item):
        if item:
            return item.tags.values_list('name', flat=True)
        return ()


class NewsArticleCreate(CreateView):
    model = NewsArticle
    form_class = NewsArticleForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(NewsArticleCreate, self).form_valid(form)


class NewsArticleDelete(DeleteView, OwnedObject):
    """Delete a News."""
    model = NewsArticle
    success_url = reverse_lazy('news_list_all')


class NewsArticleUpdate(UpdateView, OwnedObject):
    """Updates a NewsArticle."""
    model = NewsArticle
    form_class = NewsArticleForm

    def get_context_data(self, **kwargs):
        context = super(NewsArticleUpdate, self).get_context_data(**kwargs)
        context['page_title'] = _('Editar noticia')
        return context


class NewsArticleList(ListView, FilterableList):
    model = NewsArticle
    paginate_by = 10


class NewsArticleListTag(ListView, FilterableList):
    model = NewsArticle
    paginate_by = 10

    def get_queryset(self):
        tag = self.kwargs['tag']
        filter_news = NewsArticle.objects.filter(
            tags__slug__in=[tag]).distinct()

        return filter_news
