from factory import SubFactory
from factory.django import DjangoModelFactory

from events.tests.factories import UserFactory
from pycompanies.models import Company, UserCompanyProfile


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    owner = SubFactory(UserFactory)
    rank = 1


class UserCompanyProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserCompanyProfile

    user = SubFactory(UserFactory)
    company = SubFactory(CompanyFactory)
