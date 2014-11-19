from django.shortcuts import render, redirect, get_object_or_404
from waliki.models import Page


def irc(request):
    return render(request, 'irc/irc.html')

def special_page(request, **kwargs):
    return render(request, 'special_page.html', kwargs)

def buscador(request):
    return render(request, 'buscador.html', {'buscar': request.GET.get('buscar', '')})

def old_url_redirect(request, slug):
    page = Page.objects.get(slug=slug)
    return redirect(page.get_absolute_url(), permanent=True)