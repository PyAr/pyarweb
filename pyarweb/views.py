from django.http import Http404
from django.shortcuts import render, redirect
from waliki.models import Page, Redirect


def irc(request):
    return render(request, 'irc/irc.html')


def special_page(request, **kwargs):
    return render(request, 'special_page.html', kwargs)


def buscador(request):
    return render(request, 'buscador.html', {'buscar': request.GET.get('buscar', '')})


def old_url_redirect(request, slug):

    try:
        redirect = Redirect.objects.get(old_slug=slug)
        slug = redirect.new_slug
    except Redirect.DoesNotExist:
        pass

    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        raise Http404

    return redirect(page.get_absolute_url(), permanent=True)