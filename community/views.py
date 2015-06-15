# -*- coding: utf-8 -*-


"""Handle the Views of the Homepage and others."""


from django.http import Http404
from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.utils.translation import ugettext_lazy as _
from jobs.models import Job
from news.models import NewsArticle


def homepage(request):
    news = NewsArticle.objects.order_by('-created')[:3]
    jobs = Job.objects.order_by('-created')[:3]
    return render(request, 'community/index.html',
                  {'news': news, 'jobs': jobs})


def learning(request):
    title = _('Aprendiendo Python')
    return render(request, 'special_page.html', {'title': title, 'slug': 'AprendiendoPython'})


def about_pyar(request):
    title = _('Acerca de PyAr')
    return render(request, 'special_page.html', {'title': title, 'slug': 'QuienesSomos'})


def members(request):
    title = _('¿Dónde viven los miembros de PyAr?')
    return render(request, 'special_page.html', {'title': title, 'slug': 'MiembrosDePyAr'})


def mailing_list(request):
    title = _('Lista de Correo')
    return render(request, 'special_page.html', {'title': title, 'slug': 'ListaDeCorreo'})


class OwnedObject(SingleObjectMixin):

    """An object that needs to verify current user ownership
        before allowing manipulation. """

    def get_object(self, *args, **kwargs):
        obj = super(OwnedObject, self).get_object(*args, **kwargs)
        try:
            if not obj.owner == self.request.user:
                raise Http404()
        except AttributeError:
            pass
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
        object_list = self.model.objects
        included = self.included_tags
        excluded = self.excluded_tags
        if included:
            return object_list.filter(
                tags__name__in=included).distinct()
        if excluded:
            return object_list.exclude(
                tags__name__in=excluded).distinct()
        return object_list.all()

    def get_context_data(self, **kwargs):
        context = super(FilterableList, self).get_context_data(**kwargs)
        context['tags'] = self.model.tags.all()
        context['included'] = self.included_tags
        context['excluded'] = self.excluded_tags
        return context
