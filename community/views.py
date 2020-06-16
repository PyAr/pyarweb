# -*- coding: utf-8 -*-


"""Handle the Views of the Homepage and others."""

from django.db.models import F, Value, CharField
from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.utils.timezone import now
from events.models import Event
from jobs.models import Job
from news.models import NewsArticle

RECENT_ITEMS_LEN = 10


# Auxiliary function for the homepage context
def aux_qs_to_list_for_context(qs):
    """Cast the given QuerySet to a list with at most RECENT_ITEMS_LEN elements"""
    return list(qs[:RECENT_ITEMS_LEN])


class HomePageView(TemplateView):
    template_name = "community/index.html"

    def get_events_for_context(self):
        """Ensure events have 'category', created' and 'title' fields"""
        events = Event.objects.filter(start_at__lt=now())
        events = events.order_by('-start_at')
        events = events.annotate(
            created=F('start_at'),
            title=F('name'),
            category=Value('Eventos', output_field=CharField()))
        return aux_qs_to_list_for_context(events)

    def get_jobs_for_context(self):
        """Ensure jobs have a 'category' field"""
        jobs = Job.objects.order_by('-created')
        jobs = jobs.annotate(category=Value('Trabajos', output_field=CharField()))
        return aux_qs_to_list_for_context(jobs)

    def get_news_for_context(self):
        """Ensure news have 'category' and 'description' fields"""
        news = NewsArticle.objects.order_by('-created')
        news = news.annotate(
            description=F('body'),
            category=Value('Noticias', output_field=CharField()))
        return aux_qs_to_list_for_context(news)

    def get_context_data(self, **kwargs):
        """Add to the template context a list of the most recent events, jobs and news"""
        news = self.get_news_for_context()
        jobs = self.get_jobs_for_context()
        events = self.get_events_for_context()
        # Sort the last news, jobs and events to define the definitive 'recent' list
        recent = sorted(news + jobs + events, key=lambda r: r.created, reverse=True)

        context = super(HomePageView, self).get_context_data(**kwargs)
        context['recent'] = recent[:RECENT_ITEMS_LEN]
        return context


homepage = HomePageView.as_view()


def validate_obj_owner(obj, user):
    """ Auxiliary function that raises Http404 if the given user is not the
    obj.owner
    """
    try:
        if not obj.owner == user:
            raise Http404()
    except AttributeError:
        pass
    return obj


class OwnedObject(SingleObjectMixin):
    """An object that needs to verify current user ownership
        before allowing manipulation. """

    def get_object(self, *args, **kwargs):
        obj = super(OwnedObject, self).get_object(*args, **kwargs)
        return validate_obj_owner(obj, self.request.user)


class FilterableList(MultipleObjectMixin):

    """A list of objects whose queryset depends on excluded
        and included tags in the request. """

    def dispatch(self, request, *args, **kwargs):
        self.included_tags = list()
        self.excluded_tags = list()
        for k, v in request.GET.items():
            if k.startswith('tag_'):
                if v == '1':
                    self.included_tags.append(k[4:])
                elif v == '2':
                    self.excluded_tags.append(k[4:])
        return super(FilterableList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        obj_list = super(FilterableList, self).get_queryset()
        included = self.included_tags
        excluded = self.excluded_tags
        if included:
            obj_list = obj_list.filter(tags__slug__in=included).distinct()
        if excluded:
            obj_list = obj_list.exclude(tags__slug__in=excluded).distinct()
        return obj_list

    def get_context_data(self, **kwargs):
        context = super(FilterableList, self).get_context_data(**kwargs)
        context['tags'] = self.model.tags.all()
        context['included'] = self.included_tags
        context['excluded'] = self.excluded_tags
        return context
