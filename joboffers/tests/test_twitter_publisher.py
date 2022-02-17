from unittest.mock import patch

import tweepy
from requests_mock.exceptions import NoMockAddress
from requests_mock.mocker import Mocker

from ..publishers.twitter import ERROR_LOG_MESSAGE_AUTH, ERROR_LOG_MESSAGE_POST, TwitterPublisher

DUMMY_MESSAGE = 'message'
DUMMY_EXCEPTION_MESSAGE = 'Oops'
DUMMY_BAD_REQUEST_TEXT = 'This is bad'


class JsonError:
    status_code = 401
    reason = DUMMY_BAD_REQUEST_TEXT

    def json():
        return {}


class DummyAPI:

    def update_status(*args, **kwargs):
        raise tweepy.errors.Unauthorized(JsonError)

#def requests_mock: Mocker):
def test_push_to_api_wrong_credential_format(settings, caplog):
    """Test exception when the credentials are in the wrong format."""
    settings.TWITTER_CONSUMER_KEY = 123
    settings.TWITTER_CONSUMER_SECRET = 123
    settings.TWITTER_ACCESS_TOKEN = 123
    settings.TWITTER_ACCESS_SECRET = 123
    status = TwitterPublisher()._push_to_api('message')
    expected_error_message = ERROR_LOG_MESSAGE_AUTH % (
                                                        str(settings.TWITTER_CONSUMER_KEY),
                                                        str(settings.TWITTER_CONSUMER_SECRET),
                                                        str(settings.TWITTER_ACCESS_TOKEN),
                                                        str(settings.TWITTER_ACCESS_SECRET),
                                                        '')

    assert expected_error_message in caplog.text
    assert status == None


@patch(
        'joboffers.publishers.twitter.tweepy.API',
    )
def test_push_to_api_bad_credentials(mock_api, settings, caplog):
    """Test exception when the credentials are in the wrong format."""
    mock_api.return_value = DummyAPI
    status = TwitterPublisher()._push_to_api('message')
    expected_error_message = ERROR_LOG_MESSAGE_POST % (
                                                        settings.TWITTER_CONSUMER_KEY,
                                                        settings.TWITTER_CONSUMER_SECRET,
                                                        settings.TWITTER_ACCESS_TOKEN,
                                                        settings.TWITTER_ACCESS_SECRET,
                                                        '')

    assert expected_error_message in caplog.text
    assert status == 401
