import pytest

from events.tests.factories import DEFAULT_USER_PASSWORD
from pycompanies.tests.fixtures import create_user_company_profile  # noqa
from pyarweb.tests.fixtures import create_client # noqa


@pytest.fixture(name='publisher_client')
def create_publisher_client(client, user_company_profile):
    """
    Django client fixture with a logged publisher user
    """
    user = user_company_profile.user
    print('user_company_profile.user:', user)
    assert client.login(username=user.username, password=DEFAULT_USER_PASSWORD)

    return client
