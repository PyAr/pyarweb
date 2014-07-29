from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.http import HttpResponseForbidden
from news.models import NewsArticle


def homepage(request):
    news = NewsArticle.objects.order_by('-created')[:3]
    return render(request, 'community/index.html', {'news': news})


class OwnedObject(SingleObjectMixin):

    """An object that needs to verify current user ownership
        before allowing manipulation. """

    def get_object(self, *args, **kwargs):
        obj = super(OwnedObject, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise HttpResponseForbidden
        return obj


class FilterableList(MultipleObjectMixin):

    """A list of objects whose queryset depends on excluded
        and included tags in the request. """

    def dispatch(self, request, *args, **kwargs):
        self.included_tags = []
        self.excluded_tags = []
        for k, v in request.GET.items():
            if k.startswith('tag_'):
                if v == '1':
                    self.included_tags.append(k[4:])
                elif v == '2':
                    self.excluded_tags.append(k[4:])
        return super(FilterableList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        object_list = self.model.objects.order_by('-created')
        included = self.included_tags
        excluded = self.excluded_tags
        if included:
            object_list = object_list.filter(
                tags__name__in=included).distinct()
        if excluded:
            object_list = object_list.exclude(
                tags__name__in=excluded).distinct()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(FilterableList, self).get_context_data(**kwargs)
        context['tags'] = self.model.tags.all()
        context['included'] = self.included_tags
        context['excluded'] = self.excluded_tags
        return context
