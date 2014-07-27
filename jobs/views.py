from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Job
from .forms import JobForm


class JobCreate(CreateView):
    model = Job
    form_class = JobForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(JobCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(JobCreate, self).get_context_data(**kwargs)
        context['page_title'] = _('Agregar trabajo')
        return context


class JobList(ListView):
    model = Job
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        self.included_tags = []
        self.excluded_tags = []
        for k, v in request.GET.items():
            if k.startswith('tag_'):
                if v == '1':
                    self.included_tags.append(k[4:])
                elif v == '2':
                    self.excluded_tags.append(k[4:])
        return super(JobList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        job_list = Job.objects.order_by('-created')
        included = self.included_tags
        excluded = self.excluded_tags
        if included:
            job_list = job_list.filter(tags__name__in=included).distinct()
        if excluded:
            job_list = job_list.exclude(tags__name__in=excluded).distinct()
        return job_list

    def get_context_data(self, **kwargs):
        context = super(JobList, self).get_context_data(**kwargs)
        context['tags'] = Job.tags.all()
        context['included'] = self.included_tags
        context['excluded'] = self.excluded_tags
        return context


class JobUpdate(UpdateView):

    """Edit jobs that use Python."""
    model = Job
    form_class = JobForm

    def get_object(self, *args, **kwargs):
        job = super(JobUpdate, self).get_object(*args, **kwargs)
        if not job.owner == self.request.user:
            raise HttpResponseForbidden
        return job

    def get_context_data(self, **kwargs):
        context = super(JobUpdate, self).get_context_data(**kwargs)
        context['page_title'] = _('Editar trabajo')
        return context


class JobDelete(DeleteView):

    """Delete a Job."""
    model = Job
    success_url = reverse_lazy('jobs_list_all')

    def get_object(self, *args, **kwargs):
        job = super(JobDelete, self).get_object(*args, **kwargs)
        if not job.owner == self.request.user:
            raise HttpResponseForbidden
        return job
