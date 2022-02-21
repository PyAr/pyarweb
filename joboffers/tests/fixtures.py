import pytest

from events.tests.factories import UserFactory


@pytest.fixture(name='publisher_client')
def create_publisher_client(client, user_company_profile):
    """
    Django client fixture with a logged publisher user
    """
    user = user_company_profile.user
    client.force_login(user)

    return client


@pytest.fixture(name='admin_user')
def create_admin_user():
    """
    Create and return a random admin user
    """
    return UserFactory(is_superuser=True)


@pytest.fixture(name='admin_client')
def create_admin_client(client, admin_user):
    """
    Django client fixture with a logged admin user
    """
    client.force_login(admin_user)

    return client
