import pytest
from django.test import Client
from events.tests.factories import UserFactory, DEFAULT_USER_PASSWORD


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
    assert client.login(username=user.username, password=DEFAULT_USER_PASSWORD)
    return client


@pytest.fixture(name='moderator_user')
def create_moderator_user():
    """
    Create and return a random admin user
    """
    return UserFactory(is_superuser=True)


@pytest.fixture(name='moderator_client')
def create_moderator_client(client, moderator_user):
    """
    Django client fixture with a logged admin user
    """
    assert client.login(username=moderator_user.username, password=DEFAULT_USER_PASSWORD)

    return client
