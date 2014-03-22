from django.shortcuts import render
from .models import Question


def list_all(request):
    """Return all FAQs ordered by topic."""

    faqs_list = Question.objects.filter(active=True).order_by('topic')

    context = dict(faqs=faqs_list)
    return render(request, 'faq/all.html', context)
