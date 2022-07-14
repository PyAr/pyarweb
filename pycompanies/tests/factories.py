from factory import Faker, Sequence, SubFactory
from factory.django import DjangoModelFactory, ImageField

from events.tests.factories import UserFactory
from pycompanies.models import Company, UserCompanyProfile


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = Sequence(lambda n: f'company-{n}')
    photo = ImageField(color='blue')
    description = Faker('text')
    link = Faker('url')
    rank = 1


class UserCompanyProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserCompanyProfile

    user = SubFactory(UserFactory)
    company = SubFactory(CompanyFactory)
