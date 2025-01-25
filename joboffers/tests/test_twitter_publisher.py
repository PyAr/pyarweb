from unittest.mock import patch

import tweepy

from ..publishers.twitter import (
    ERROR_LOG_MESSAGE_POST,
    TwitterPublisher,
    _repr_credentials,
)

DUMMY_MESSAGE = 'message'
DUMMY_TITLE = 'title'
DUMMY_LINK = 'https://example.com'
DUMMY_EXCEPTION_MESSAGE = 'Oops'
DUMMY_BAD_REQUEST_TEXT = 'This is bad'


class JsonError:
    status_code = 401
    reason = DUMMY_BAD_REQUEST_TEXT

    def json():
        return {}


class DummyAPIBad:
    def update_status(*args, **kwargs):
        raise tweepy.errors.Unauthorized(JsonError)


class DummyAPIOK:
    def update_status(*args, **kwargs):
        return


def test_push_to_api_wrong_credential_format(settings, caplog):
    """Test exception when the credentials are in the wrong format."""
    settings.TWITTER_CONSUMER_KEY = 123
    settings.TWITTER_CONSUMER_SECRET = 123
    settings.TWITTER_ACCESS_TOKEN = 123
    settings.TWITTER_ACCESS_SECRET = 123
    status = TwitterPublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)
    expected_error_message = 'Consumer key must be string or bytes'

    assert expected_error_message in caplog.text
    assert status is None


@patch(
    'joboffers.publishers.twitter.tweepy.API',
)
def test_push_to_api_bad_credentials_None(mock_api, settings, caplog):
    """Test exception when the credentials are not set."""
    mock_api.return_value = DummyAPIBad
    settings.TWITTER_ACCESS_SECRET = None
    settings.TWITTER_ACCESS_TOKEN = None
    settings.TWITTER_ACCESS_SECRET = None
    settings.TWITTER_CONSUMER_KEY = None

    status = TwitterPublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)
    assert status is None


@patch(
    'joboffers.publishers.twitter.tweepy.API',
)
def test_push_to_api_bad_credentials(mock_api, settings, caplog):
    """Test exception when the credentials are in the wrong format."""
    mock_api.return_value = DummyAPIBad
    settings.TWITTER_ACCESS_SECRET = ''
    settings.TWITTER_ACCESS_TOKEN = ''
    settings.TWITTER_CONSUMER_SECRET = ''
    settings.TWITTER_CONSUMER_KEY = ''

    status = TwitterPublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)
    expected_error_message = ERROR_LOG_MESSAGE_POST % (_repr_credentials(), '')

    assert expected_error_message in caplog.text
    assert status == 401


@patch(
    'joboffers.publishers.twitter.tweepy.API',
)
def test_push_to_api_ok(mock_api, settings):
    mock_api.return_value = DummyAPIOK

    settings.TWITTER_ACCESS_SECRET = ''
    settings.TWITTER_ACCESS_TOKEN = ''
    settings.TWITTER_CONSUMER_SECRET = ''
    settings.TWITTER_CONSUMER_KEY = ''

    status = TwitterPublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)

    assert status == 200
