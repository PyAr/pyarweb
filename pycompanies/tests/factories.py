from factory import SubFactory, Faker
from factory.django import DjangoModelFactory

from pycompanies.models import Company, UserCompanyProfile
from events.tests.factories import UserFactory


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
