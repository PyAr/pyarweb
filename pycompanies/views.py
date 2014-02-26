from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Company
from .forms import CompanyForm


@login_required
def add(request):
    """Add a new Company."""
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            url = reverse('companies_list_all')
            return HttpResponseRedirect(url)
    else:
        form = CompanyForm()

    context = dict(form=form)
    return render(request, 'companies/add.html', context)


def list_all(request):
    """Return all news Company ordered by date desc."""
    companies = Company.objects.order_by('-created')
    context = dict(companies=companies)
    return render(request, 'companies/all.html', context)

@login_required
def edit(request, company_id=None):
    """Edit Companies that use Python."""
    if company_id:
        company = get_object_or_404(Company, id=company_id)
        if request.POST and company.owner == request.user:
            form = CompanyForm(request.POST, instance=company)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/companies')
        if company.owner != request.user:
            return HttpResponseForbidden()
        form = CompanyForm(instance=company)
        context = dict(form=form)
        return render(request, 'companies/edit.html', context)
    else:
        companies = Company.objects.filter(owner=request.user)
        context = dict(companies=companies)
        return render(request, 'companies/companies_by_user.html', context)

