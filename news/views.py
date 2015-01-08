from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView
from django.utils.translation import ugettext as _
from community.views import OwnedObject, FilterableList
from .models import NewsArticle
from .forms import NewsArticleForm


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
