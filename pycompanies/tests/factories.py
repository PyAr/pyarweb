from factory import SubFactory
from factory.django import DjangoModelFactory

from pycompanies.models import Company
from events.tests.factories import UserFactory


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    owner = SubFactory(UserFactory)
    rank = 1
