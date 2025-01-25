import urllib.parse

from requests_mock.exceptions import NoMockAddress
from requests_mock.mocker import Mocker
from unittest.mock import MagicMock, patch

from joboffers.constants import TELEGRAM_SENDING_ERROR
from joboffers.models import JobOffer
from joboffers.telegram_api import (
  _compose_message,
  _get_request_url,
  TELEGRAM_API_URL,
  send_message,
  send_notification_to_moderators
)


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


def test_logging_failing_send_message(requests_mock: Mocker, caplog):
    """Test that failing sendind a messages creates a log entry"""
    message = 'this is a test'
    safe_message = _compose_message(message)
    chat_id = 1
    url = _get_request_url(safe_message, chat_id)
    requests_mock.get(url, json='', status_code=404)

    send_message(message, chat_id)
    assert len(caplog.records) == 1


@patch("joboffers.telegram_api.messages")
def test_messages_failing_send_message(mocked_messages, requests_mock):
    """Test that failing sendind a messages creates a log entry"""
    message = 'this is a test'
    safe_message = _compose_message(message)
    chat_id = 1
    url = _get_request_url(safe_message, chat_id)
    requests_mock.get(url, json='', status_code=404)
    request = MagicMock()

    send_message(message, chat_id, request)

    assert mocked_messages.add_message.called
    assert mocked_messages.add_message.call_args[0][1] == TELEGRAM_SENDING_ERROR


def test_send_notification_to_moderators(settings):
    """Test that message has been crafted correctly."""
    dummy_job_slug = 'python-job'
    dummy_message = 'dummy message'
    dummy_chat_id = 1

    settings.TELEGRAM_MODERATORS_CHAT_ID = dummy_chat_id

    offer = JobOffer(slug=dummy_job_slug)
    expected_message = offer.get_full_url()

    with patch('joboffers.telegram_api.send_message') as mock_send_message:
        send_notification_to_moderators(dummy_message)
        assert mock_send_message.called_args(expected_message, dummy_chat_id)
