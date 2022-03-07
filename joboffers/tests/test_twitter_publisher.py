from unittest.mock import patch

import tweepy

from ..publishers.twitter import (ERROR_LOG_MESSAGE_POST, TwitterPublisher,
                                  _repr_credentials)

DUMMY_MESSAGE = 'message'
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
    status = TwitterPublisher()._push_to_api('message')
    expected_error_message = 'Consumer key must be string or bytes'

    assert expected_error_message in caplog.text
    assert status is None


@patch(
    'joboffers.publishers.twitter.tweepy.API',
)
def test_push_to_api_bad_credentials(mock_api, settings, caplog):
    """Test exception when the credentials are in the wrong format."""
    mock_api.return_value = DummyAPIBad
    status = TwitterPublisher()._push_to_api('message')
    expected_error_message = ERROR_LOG_MESSAGE_POST % (_repr_credentials(), '')

    assert expected_error_message in caplog.text
    assert status == 401


@patch(
    'joboffers.publishers.twitter.tweepy.API',
)
def test_push_to_api_ok(mock_api):
    mock_api.return_value = DummyAPIOK

    status = TwitterPublisher()._push_to_api('message')

    assert status == 200
