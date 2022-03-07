import urllib.parse

from requests_mock.exceptions import NoMockAddress
from requests_mock.mocker import Mocker

from ..telegram_api import TELEGRAM_API_URL, _compose_message, _get_request_url, send_message


def test_get_request_url(settings):
    """Test the correct structure for the API request url."""
    message = 'dummy_message'
    chat_id = 1
    dummy_token = '12345'
    settings.TELEGRAM_BOT_TOKEN = dummy_token
    expected_url = (
        f'{TELEGRAM_API_URL}{dummy_token}/sendMessage?chat_id={chat_id}&text={message}'
    )
    result = _get_request_url(message, chat_id)
    assert result == expected_url


def test_compose_message(settings):
    """Test santitizing escaping and adding a prefix to a message."""
    dummy_message = 'this is a test'
    dummy_prefix = 'test'
    settings.TELEGRAM_MESSAGE_PREFIX = dummy_prefix

    result_message = _compose_message(dummy_message)
    message_with_prefix = f'{dummy_prefix} {dummy_message}'
    safe_message = urllib.parse.quote_plus(message_with_prefix)
    assert result_message == safe_message


def test_send_message(requests_mock: Mocker):
    """Test that the message send to telegram, has the right structure."""
    message = 'this is a test'
    safe_message = _compose_message(message)
    chat_id = 1
    url = _get_request_url(safe_message, chat_id)
    requests_mock.get(url, json='', status_code=200)

    try:
        send_message(message, chat_id)
    except NoMockAddress:
        assert (
            False
        ), 'Send Message raised an exception, wich means that the url is malformed.'
