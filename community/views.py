from django.shortcuts import render


def homepage(request):
    return render(request, 'community/index.html')
