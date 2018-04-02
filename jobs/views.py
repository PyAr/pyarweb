import datetime
from dateutil.relativedelta import relativedelta
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView
from django.contrib.syndication.views import Feed
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from community.views import OwnedObject, FilterableList, FilterQuerySetMixin
from .models import Job, JobInactivated
from .forms import JobForm, JobInactivateForm, JobSearchForm
from pyarweb.settings import DEFAULT_FROM_EMAIL


class JobActiveMixin(object):
    def get_queryset(self):
        """ Job must be active """
        qs = super(JobActiveMixin, self).get_queryset()
        return qs.actives()


class JobsFeed(Feed):
    title = "Feed de ofertas laborales de Pyar"
    link = reverse_lazy("jobs_list_all")
    description = "Todas las ofertas laborales con Python publicadas en PyAR"

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


class JobList(ListView, JobActiveMixin, FilterQuerySetMixin, FilterableList):
    model = Job
    paginate_by = 20
    filter_fields = {
        'title': 'title__icontains',
        'location': 'location__icontains',
        'seniority': 'seniority',
        'remote_work': 'remote_work',
        'company': 'company'
    }

    def get_context_data(self, **kwargs):
        context = super(JobList, self).get_context_data(**kwargs)
        context['search_jobs_form'] = JobSearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        qry = super(JobList, self).get_queryset()
        if 'created' in self.request.GET:
            today = datetime.datetime.today()
            if 'today' in self.request.GET['created']:
                qry = qry.filter(created__year=today.year, created__month=today.month,
                                 created__day=today.day)
            elif 'yesterday' in self.request.GET['created']:
                yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
                qry = qry.filter(created__year=yesterday.year, created__month=yesterday.month,
                                 created__day=yesterday.day)
            elif 'last_3_days' in self.request.GET['created']:
                last_3_days = datetime.datetime.today() - datetime.timedelta(days=3)
                qry = qry.filter(created__lt=today, created__gt=last_3_days)
            elif 'last_week' in self.request.GET['created']:
                last_week = datetime.datetime.today() - datetime.timedelta(days=7)
                qry = qry.filter(created__lt=today, created__gt=last_week)
            elif 'month_ago' in self.request.GET['created']:
                month_ago = datetime.datetime.now() - relativedelta(months=1)
                qry = qry.filter(created__range=[month_ago, today])

        return qry


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
            context = {
                'job_title': job.title,
                'reason': form.cleaned_data['reason'],
                'comment': form.cleaned_data['comment']
            }

            body = render_to_string('jobs/inactivate_job_email.txt', context)
            email = EmailMessage(
                subject="[PyAr] Aviso de trabajo dado de baja",
                to=(job.company.owner.email, ),
                from_email=DEFAULT_FROM_EMAIL,
                body=body
            )
            email.send()

        return super(JobInactivate, self).form_valid(form)
