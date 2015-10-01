from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView
from django.contrib.syndication.views import Feed
from community.views import OwnedObject, FilterableList
from .models import Job, JobInactivated
from .forms import JobForm, JobInactivateForm


class JobActiveMixin(object):
    def get_queryset(self):
        """ Job must be active """
        qs = super(JobActiveMixin, self).get_queryset()
        return qs.actives()


class JobsFeed(Feed):
    title = "Feed de ofertas laborales de Pyar"
    link = reverse_lazy("jobs_list_all")
    description = "Todas las ofertas laborales con Python publicadas en Python Argentina"

    description_template = "jobs/job_detail_feed.html"

    def items(self):
        return Job.objects.order_by('-created')[0:10]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.created

    def author_name(self, item):
        if item and item.company:
            return item.company.name
        return ''

    def author_email(self, item):
        if item:
            return item.email
        return ''

    def author_link(self, item):
        if item and item.company:
            return item.company.get_absolute_url()
        return ''

    def categories(self, item):
        if item:
            return item.tags.values_list('name', flat=True)
        return ()


class JobCreate(CreateView):
    model = Job
    form_class = JobForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_active = True
        return super(JobCreate, self).form_valid(form)


class JobList(ListView, JobActiveMixin, FilterableList):
    model = Job
    paginate_by = 20


class JobUpdate(UpdateView, JobActiveMixin, OwnedObject):

    """Edit jobs that use Python."""
    model = Job
    form_class = JobForm


class JobDelete(DeleteView, JobActiveMixin, OwnedObject):

    """Delete a Job."""
    model = Job
    success_url = reverse_lazy('jobs_list_all')


class JobInactivate(CreateView):
    """ Inactivate Job by moderator """

    model = JobInactivated
    template_name = 'jobs/job_inactivate_form.html'
    form_class = JobInactivateForm

    def form_valid(self, form):
        job = Job.objects.get(pk=self.kwargs['pk'])
        form.instance.job = job

        # -- inactivate job
        job.is_active = False
        job.save()

        # -- ¿send mail to job owner?
        if form.cleaned_data['send_email']:
            print(job.company.owner.email)

        return super(JobInactivate, self).form_valid(form)
