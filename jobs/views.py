from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Job
from .forms import JobForm


@login_required
def add(request):
    """Add a new Job."""
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            url = reverse('jobs_list_all')
            return HttpResponseRedirect(url)
    else:
        form = JobForm()

    context = dict(form=form)
    return render(request, 'jobs/add.html', context)


def list_all(request):
    """Return all news Jobs ordered by date desc."""
    jobs = Job.objects.order_by('-created')
    context = dict(jobs=jobs)
    return render(request, 'jobs/all.html', context)

@login_required
def update(request, job_id=None):
    """Edit Jobs that use Python."""
    if job_id:
        job = get_object_or_404(Job, id=job_id)
        if request.POST and job.owner == request.user:
            form = JobForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                form.save_m2m()
                return HttpResponseRedirect('/jobs')
        if job.owner != request.user:
            return HttpResponseForbidden()
        form = JobForm(instance=job)
        context = dict(form=form)
        return render(request, 'jobs/edit.html', context)
    else:
        jobs = Job.objects.filter(owner=request.user)
        context = dict(jobs=jobs)
        return render(request, 'jobs/jobs_by_user.html', context)


@login_required
def delete(request, job_id):
    """Delete a Job."""

    job = get_object_or_404(
        Job,
        id=job_id,
        owner=request.user,
    )
    job.delete()
    url = reverse('jobs_list_all')

    return HttpResponseRedirect(url)


def view(request, job_id):
    """Show a Job."""

    job = get_object_or_404(
        Job,
        id=job_id
    )

    context = dict(job=job)
    return render(request, 'jobs/view.html', context)