import pytest
import re

from requests_mock import ANY

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


class DummyTelegram(object):
    """
    Convenience wrapper of requests mock to simulate telegram responses and tests messages sent
    """
    def __init__(self, requests_mock):
        self.requests_mock = requests_mock

    @property
    def call_history(self):
        return [history.qs for history in self.requests_mock.request_history]


@pytest.fixture(name='telegram_dummy')
def create_telegram_dummy(requests_mock, settings):
    settings.TELEGRAM_BOT_TOKEN = '12345'
    settings.TELEGRAM_MESSAGE_PREFIX = '[TEST]'
    settings.TELEGRAM_MODERATORS_CHAT_ID = 1

    matcher = re.compile(r'api.telegram.org/bot.*$')
    requests_mock.register_uri(ANY, matcher, text='dummy response')

    return DummyTelegram(requests_mock)
