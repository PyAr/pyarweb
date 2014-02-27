from django.shortcuts import render

def irc(request):
    return render(request, 'irc/irc.html')
