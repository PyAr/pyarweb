from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from events.tests.factories import UserFactory
from pycompanies.models import Company, UserCompanyProfile


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = Sequence(lambda n: f'company-{n}')
    owner = SubFactory(UserFactory)
    rank = 1


class UserCompanyProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserCompanyProfile

    user = SubFactory(UserFactory)
    company = SubFactory(CompanyFactory)
