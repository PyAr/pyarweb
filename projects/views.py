# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Project
from .forms import ProjectForm


@login_required
def add(request):
    """Add a new Project."""

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            url = reverse('projects_list_all')
            return HttpResponseRedirect(url)
    else:
        form = ProjectForm()

    context = dict(form=form)
    return render(request, 'projects/add.html', context)


def view(request, project_id):
    """Show a Project."""

    project = get_object_or_404(
        Project,
        id=project_id
    )

    context = dict(project=project)
    return render(request, 'projects/view.html', context)


@login_required
def delete(request, project_id):
    """Delete a Project."""

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user,
    )
    project.delete()
    url = reverse('projects_list_all')

    return HttpResponseRedirect(url)


@login_required
def update(request, project_id):
    """Update a Project."""

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user,
    )

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            url = reverse('projects_list_all')
            return HttpResponseRedirect(url)
    else:
        form = ProjectForm(instance=project)

    context = dict(
        form=form,
        project=project
    )
    return render(request, 'projects/update.html', context)


def list_all(request):
    """Return all projects ordered by name."""

    projects_list = Project.objects.order_by('name')
    paginator = Paginator(projects_list, 20) # Show 20 projects per page
    page = request.GET.get('page')

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        projects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        projects = paginator.page(paginator.num_pages)

    context = dict(projects=projects)
    return render(request, 'projects/all.html', context)


