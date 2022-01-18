import pytest

from django.test import Client

from events.tests.factories import UserFactory, DEFAULT_USER_PASSWORD
from pycompanies.tests.factories import UserCompanyProfileFactory


@pytest.fixture(name='client')
def create_client():
    return Client()


@pytest.fixture(name='user')
def create_user():
    return UserFactory()


@pytest.fixture(name='logged_client')
def create_logged_client(user):
    client = Client()
    client.login(username=user.username, password=DEFAULT_USER_PASSWORD)
    return client


@pytest.fixture(name='user_company_profile')
def create_user_company_profile():
    """
    Fixture with a dummy UserCompanyProfileFactory
    """
    return UserCompanyProfileFactory.create()
