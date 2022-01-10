from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from pycompanies.models import Company, UserCompanyProfile
from events.tests.factories import UserFactory


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = Faker('company')
    owner = SubFactory(UserFactory)
    rank = 1


class UserCompanyProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserCompanyProfile

    user = SubFactory(UserFactory)
    company = SubFactory(CompanyFactory)
