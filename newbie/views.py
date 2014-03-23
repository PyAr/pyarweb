from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import PadawanForm, JediForm
from .models import Jedi, Padawan


@login_required
def add_padawan(request):
    """ Add a new Padawan """
    form = PadawanForm(request.POST or None)
    if form.is_valid():
        padawan = form.save(commit=False)
        padawan.user = request.user
        padawan.save()
        form.save_m2m()

    context = dict(form=form)
    return render(request, 'newbie/add-padawan.html', context)


@login_required
def add_jedi(request):
    """ Add a new Jedi """
    form = JediForm(request.POST or None)
    if form.is_valid():
        form.save()


    context = dict(form=form)
    return render(request, 'newbie/add-jedi.html', context)


def list_jedi(request):
    """ List Jedi """
    jedi_list = Jedi.objects.all()
    context = {
        "jedi_list": jedi_list
    }

    return render(request, 'newbie/list-jedi.html', context)


def list_padawan(request):
    """ List Jedi """
    padawan_list = Padawan.objects.all()
    context = {
        "padawan_list": padawan_list
    }
    return render(request, 'newbie/list-padawan.html', context)
