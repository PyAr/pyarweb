from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from .models import Project, Mentor, Apprentice, Project
from .forms import MentorForm, ApprenticeForm, ProjectForm


class AddMentor(CreateView):
    model = Mentor
    form_class = MentorForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddMentor, self).form_valid(form)


class DisplayMentor(DetailView):
    model = Mentor
    form_class = MentorForm

    def get_context_data(self, **kwargs):
        context = super(DisplayMentor, self).get_context_data(**kwargs)
        return context


class UpdateMentor(UpdateView):
    model = Mentor
    form_class = MentorForm


class DeleteMentor(DeleteView):
    model = Mentor
    success_url = reverse_lazy('new_mentor')


class AddApprentice(CreateView):
    model = Apprentice
    form_class = ApprenticeForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddApprentice, self).form_valid(form)


class DisplayApprentice(DetailView):
    model = Apprentice
    form_class = ApprenticeForm

    def get_context_data(self, **kwargs):
        context = super(DisplayApprentice, self).get_context_data(**kwargs)
        return context


class UpdateApprentice(UpdateView):
    model = Apprentice
    form_class = ApprenticeForm


class DeleteApprentice(DeleteView):
    model = Apprentice
    success_url = reverse_lazy('new_apprentice')


class AddProject(CreateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AddProject, self).form_valid(form)


class DisplayProject(DetailView):
    model = Project
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super(DisplayProject, self).get_context_data(**kwargs)
        return context


class UpdateProject(UpdateView):
    model = Project
    form_class = ProjectForm


class DeleteProject(DeleteView):
    model = Project
    success_url = reverse_lazy('new_project')
