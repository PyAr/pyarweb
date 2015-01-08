# -*- coding: utf-8 -*-


"""Views for PyArWeb Django App."""


from django.http import Http404
from django.shortcuts import redirect, render
from waliki.models import Page, Redirect


def irc(request):
    """Render the IRC Chat template."""
    return render(request, 'irc/irc.html')


def special_page(request, **kwargs):
    """Render a basic template of special pages."""
    return render(request, 'special_page.html', kwargs)


def buscador(request):
    """Render the Google Search template."""
    return render(request, 'buscador.html',
                  {'buscar': request.GET.get('buscar', '')})


def old_url_redirect(request, slug):
    """Redirect old URLs to the New site."""
    try:
        waliki_redirect = Redirect.objects.get(old_slug=slug)
        slug = waliki_redirect.new_slug
    except Redirect.DoesNotExist:
        pass

    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        raise Http404

    return redirect(page.get_absolute_url(), permanent=True)
