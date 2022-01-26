import urllib.parse
from unittest.mock import patch

from django.urls import reverse
from requests_mock.exceptions import NoMockAddress
from requests_mock.mocker import Mocker

from ..telegram_notifier import (MODERATION_MESSAGE, TELEGRAM_API_URL,
                                 _compose_message, _get_absolute_joboffer_url,
                                 _get_request_url, _send_message,
                                 send_notification_to_moderators)


def test_get_request_url(settings):
    """Test the correct strcture for the API request url."""
    message = 'dummy_message'
    chat_id = 1
    dummy_token = '12345'
    settings.TELEGRAM_BOT_TOKEN = dummy_token
    expected_url = f'{TELEGRAM_API_URL}{dummy_token}/sendMessage?chat_id={chat_id}&text={message}'
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
    requests_mock.get(url, json='', status_code=201)
    try:
        _send_message(message, chat_id)
    except NoMockAddress:
        assert False, 'Send Message raised an exception, wich means that the url is malformed.'


def test_get_absolute_joboffer_url(settings):
    """Test that the url being crafted has the correct BASE_URL and the right format."""
    dummy_url = 'http://example.com'
    dummy_job_slug = 'python-job'
    settings.BASE_URL = dummy_url
    joboffer_url = reverse('joboffers:view', kwargs={'slug': dummy_job_slug})
    expected_url = "".join((dummy_url, joboffer_url))
    result = _get_absolute_joboffer_url(dummy_job_slug)
    assert expected_url == result


def test_send_notification_to_moderators(settings):
    """Test that message has been crafted correctly."""
    dummy_job_slug = 'python-job'
    dummy_url = 'http://example.com'
    dummy_job_slug = 'python-job'
    dummy_chat_id = 1

    settings.BASE_URL = dummy_url
    settings.TELEGRAM_MODERATORS_CHAT_ID = dummy_chat_id

    joboffer_url = reverse('joboffers:view', kwargs={'slug': dummy_job_slug})
    expected_url = "".join((dummy_url, joboffer_url))
    expected_message = MODERATION_MESSAGE.format(offer_url=expected_url)

    with patch('joboffers.telegram_notifier._send_message') as mock_send_message:
        send_notification_to_moderators(dummy_job_slug)
        assert mock_send_message.called_args(expected_message, dummy_chat_id)
