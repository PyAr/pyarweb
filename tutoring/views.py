from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy
from community.views import OwnedObject, FilterableList
from django.http import HttpResponse
from .models import Project, Mentor, Apprentice, Mentorship
from .forms import MentorForm, ApprenticeForm, ProjectForm, MentorshipForm


class AddMentor(CreateView):
    model = Mentor
    form_class = MentorForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AddMentor, self).form_valid(form)


class DisplayMentor(DetailView):
    model = Mentor
    form_class = MentorForm

    def get_context_data(self, **kwargs):
        context = super(DisplayMentor, self).get_context_data(**kwargs)
        return context


class UpdateMentor(UpdateView, OwnedObject):
    model = Mentor
    form_class = MentorForm


class DeleteMentor(DeleteView, OwnedObject):
    model = Mentor
    success_url = reverse_lazy('new_mentor')


class ListMentor(ListView, FilterableList):
    model = Mentor
    paginate_by = 20


class AddApprentice(CreateView):
    model = Apprentice
    form_class = ApprenticeForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AddApprentice, self).form_valid(form)


class DisplayApprentice(DetailView):
    model = Apprentice
    form_class = ApprenticeForm

    def get_context_data(self, **kwargs):
        context = super(DisplayApprentice, self).get_context_data(**kwargs)
        return context


class UpdateApprentice(UpdateView, OwnedObject):
    model = Apprentice
    form_class = ApprenticeForm


class DeleteApprentice(DeleteView, OwnedObject):
    model = Apprentice
    success_url = reverse_lazy('new_apprentice')


class ListApprentice(ListView, FilterableList):
    model = Apprentice
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(ListApprentice, self).get_context_data(**kwargs)
        context['status_choices'] = Apprentice.STATUS_CHOICES
        return context


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


class ListProject(ListView, FilterableList):
    model = Project
    paginate_by = 20


class UpdateProject(UpdateView, OwnedObject):
    model = Project
    form_class = ProjectForm


class DeleteProject(DeleteView, OwnedObject):
    model = Project
    success_url = reverse_lazy('new_project')


class AddMentorship(CreateView):
    model = Mentorship
    form_class = MentorshipForm

    def form_valid(self, form):
        # form.instance.owner = self.request.user
        return super(AddMentorship, self).form_valid(form)


class DisplayMentorship(DetailView):
    model = Mentorship
    form_class = MentorshipForm

    def get_context_data(self, **kwargs):
        context = super(DisplayMentorship, self).get_context_data(**kwargs)
        return context


class ListMentorship(ListView):
    model = Mentorship
    paginate_by = 20


class IndexView(TemplateView):
    template_name = 'tutoring/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['mentors'] = Mentor.objects.all()
        context['apprentices'] = Apprentice.objects.all()
        context['projects'] = Project.objects.all()[:5]
        return context
