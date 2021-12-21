import pytest
from django.test import Client

from events.tests.factories import UserFactory
from pycompanies.tests.factories import UserCompanyProfileFactory


@pytest.fixture(name='client')
def create_client():
    """
    Django client fixture with anonymous user
    """
    return Client()


@pytest.fixture(name='user')
def create_user():
    """
    Dummy user fixture
    """
    return UserFactory()


@pytest.fixture(name='logged_client')
def create_logged_client(user):
    """
    Django client fixture with a logged user
    """
    client = Client()
    client.force_login(user=user)
    return client


@pytest.fixture(name='user_company_profile')
def create_user_company_profile():
    """
    Fixture with a dummy UserCompanyProfileFactory
    """
    return UserCompanyProfileFactory.create()


@pytest.fixture(name='publisher_client')
def create_publisher_client(client, user_company_profile):
    """
    Django client fixture with a logged publisher user
    """
    user = user_company_profile.user
    client.force_login(user)

    return client


@pytest.fixture(name='admin_client')
def create_admin_client(client):
    """
    Django client fixture with a logged admin user
    """
    user = UserFactory(is_superuser=True)
    client.force_login(user)

    return client
