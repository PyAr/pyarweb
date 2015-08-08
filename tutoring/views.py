from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from .models import Project, Mentor, Apprentice, Project
from .forms import MentorForm, ApprenticeForm, ProjectForm


def index(request):
    return HttpResponse('Hello stranger')

# class ProjectCreate(CreateView):
#     model = Project
#     form_class = JobForm
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super(JobCreate, self).form_valid(form)


class DisplayMentor(DetailView):
    model = Mentor
    form_class = MentorForm

    def get_context_data(self, **kwargs):
        context = super(DisplayMentor, self).get_context_data(**kwargs)
        return context


class DeleteMentor(DeleteView):
    model = Mentor
    success_url = reverse_lazy('new_mentor')


class AddMentor(CreateView):
    model = Mentor
    form_class = MentorForm
    # success_url = '/admin/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddMentor, self).form_valid(form)


class UpdateMentor(UpdateView):
    model = Mentor
    form_class = MentorForm


class AddApprentice(CreateView):
    model = Apprentice
    form_class = ApprenticeForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddApprentice, self).form_valid(form)


class AddProject(CreateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddProject, self).form_valid(form)