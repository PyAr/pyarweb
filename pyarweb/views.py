from django.shortcuts import render

def irc(request):
    return render(request, 'irc/irc.html')

def special_page(request, **kwargs):
    return render(request, 'special_page.html', kwargs)

def QuienesSomos(request):
    return render(request, 'QuienesSomos.html')


def MiembrosDePyAr(request):
    return render(request, 'MiembrosDePyAr.html')


def ListaDeCorreo(request):
    return render(request, 'ListaDeCorreo.html')
