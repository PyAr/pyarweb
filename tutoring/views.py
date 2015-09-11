from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse, reverse_lazy
from community.views import OwnedObject, FilterableList
from .models import Project, Mentor, Apprentice, Mentorship
from .forms import MentorForm, ApprenticeForm, ProjectForm, MentorshipForm
from django.views.generic.detail import SingleObjectMixin


class AddMentor(CreateView):
    model = Mentor
    form_class = MentorForm

    def dispatch(self, request, *args, **kwargs):
        try:
            mentor = Mentor.objects.get(owner=request.user)
            return redirect(reverse('update_mentor', kwargs={'slug': mentor.owner}))
        except Mentor.DoesNotExist:
            return super(AddMentor, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AddMentor, self).form_valid(form)


class DisplayMentor(DetailView):
    model = Mentor
    form_class = MentorForm
    slug_field = 'owner__username'

    def get_context_data(self, **kwargs):
        context = super(DisplayMentor, self).get_context_data(**kwargs)
        return context


class UpdateMentor(UpdateView, OwnedObject):
    model = Mentor
    form_class = MentorForm
    slug_field = 'owner__username'


# class DeleteMentor(DeleteView, OwnedObject):
#     model = Mentor
#     slug_field = 'owner__username'
#     success_url = reverse_lazy('new_mentor')


class ListMentor(ListView, FilterableList):
    model = Mentor
    paginate_by = 20


class AddApprentice(CreateView):
    model = Apprentice
    form_class = ApprenticeForm

    def dispatch(self, request, *args, **kwargs):
        try:
            apprentice = Apprentice.objects.get(owner=request.user)
            return redirect(reverse('update_apprentice', kwargs={'slug': apprentice.owner}))
        except Apprentice.DoesNotExist:
            return super(AddApprentice, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AddApprentice, self).form_valid(form)


class DisplayApprentice(DetailView):
    model = Apprentice
    form_class = ApprenticeForm
    slug_field = 'owner__username'

    def get_context_data(self, **kwargs):
        context = super(DisplayApprentice, self).get_context_data(**kwargs)
        return context


class UpdateApprentice(UpdateView, OwnedObject):
    model = Apprentice
    form_class = ApprenticeForm
    slug_field = 'owner__username'


# class DeleteApprentice(DeleteView, OwnedObject):
#     model = Apprentice
#     slug_field = 'owner__username'
#     success_url = reverse_lazy('new_apprentice')


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
#
#
# class DeleteProject(DeleteView, OwnedObject):
#     model = Project
#     success_url = reverse_lazy('new_project')


class AddMentorship(CreateView):
    model = Mentorship
    form_class = MentorshipForm

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentor'):
            return super(AddMentorship, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('new_mentor'))

    def get_form_kwargs(self):
        kwargs = super(AddMentorship, self).get_form_kwargs()
        kwargs['mentor'] = self.request.user.mentor
        return kwargs

    def form_valid(self, form):
        form.instance.owner = Mentor.objects.get(owner=self.request.user)
        return super(AddMentorship, self).form_valid(form)


class UpdateMentorship(UpdateView, SingleObjectMixin):
    model = Mentorship
    form_class = MentorshipForm

    def get_object(self, *args, **kwargs):
        obj = super(UpdateMentorship, self).get_object(*args, **kwargs)
        try:
            if not obj.owner.owner == self.request.user:
                raise Http404()
        except AttributeError:
            pass
        return obj


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
        context['mentors'] = Mentor.objects.filter(available=True)
        context['apprentices'] = Apprentice.objects.filter(status=Apprentice.STATUS_WAITING)
        context['projects'] = Project.objects.all()[:5]
        return context
