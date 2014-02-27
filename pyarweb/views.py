from django.shortcuts import render

def irc(request):
    return render(request, 'irc/irc.html')

def quienes_somos(request):
    return render(request, 'quienes_somos.html')
    
def MiembrosDePyAr(request):
    return render(request, 'MiembrosDePyAr.html')
    
def ListaDeCorreo(request):
    return render(request, 'ListaDeCorreo.html')
