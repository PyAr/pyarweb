import pytest
from django.test import Client

from events.tests.factories import UserFactory


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
