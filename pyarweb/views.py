from django.shortcuts import render

def irc(request):
    return render(request, 'irc/irc.html')

def special_page(request, **kwargs):
    return render(request, 'special_page.html', kwargs)

def buscador(request):
    return render(request, 'buscador.html', {'buscar': request.GET.get('buscar', '')})
