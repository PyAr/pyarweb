from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.http import HttpResponse
from .forms import PadawanForm, JediForm
from .models import Jedi, Padawan


@login_required
def padawan_add(request):
    """ Add a new Padawan """
    form = PadawanForm(request.POST or None)
    if form.is_valid():
        padawan = form.save(commit=False)
        padawan.user = request.user
        try:
            padawan.save()
            form.save_m2m()
        except Exception:
            return HttpResponse(_('You really are a Padawan'))

    context = dict(form=form)
    return render(request, 'newbie/add-padawan.html', context)


@login_required
def jedi_add(request):
    """ Add a new Jedi """

    form = JediForm(request.POST or None)
    if form.is_valid():
        jedi = form.save(commit=False)
        jedi.user = request.user
        try:
            jedi.save()
            form.save_m2m()
        except Exception:
            return HttpResponse(_('You really are a Jedi'))


    context = dict(form=form)
    return render(request, 'newbie/add-jedi.html', context)


def jedi_list(request):
    """ List Jedi """

    jedi_list = Jedi.objects.all()
    context = {
        "jedi_list": jedi_list
    }

    return render(request, 'newbie/list-jedi.html', context)


def padawan_list(request):
    """ List Jedi """

    padawan_list = Padawan.objects.all()
    context = {
        "padawan_list": padawan_list
    }
    return render(request, 'newbie/list-padawan.html', context)


def jedi_request(request, jedi_id):
    """ Start the process to connect with a Jedi """

    jedi = get_object_or_404(Jedi, id=jedi_id)
    padawan = get_object_or_404(Padawan, user=request.user)
    padawan.send_project_request(jedi)
    return render(request, 'newbie/jedi-request-successfully.html', {})
