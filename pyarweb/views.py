# -*- coding: utf-8 -*-


"""Views for PyArWeb Django App."""


from django.shortcuts import render


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
